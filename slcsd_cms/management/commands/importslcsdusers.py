from ldap3 import (
    Connection,
    Server,
    ALL,
    NTLM,
)
import uuid

from django.core.exceptions import ValidationError
from django.core.management.base import (
    BaseCommand,
    # CommandError
)
from django.utils import timezone
# from django.db.models import Q

from districtwebsites.settings.base import (
    get_secret,
)
from slcsd_cms.models import User

import_errors = []


def show_in_directory(item, obj):
    exclude_upn = [
        'webmaster@slcschools.org',
    ]
    exclude_department = [
        'substitute teachers',
    ]

    if str(item.userPrincipalName).lower() in exclude_upn:
        return False
    if str(item.department).lower() in exclude_department:
        return False
    if obj.non_employee:
        return False
    return True


def job_title_titlecase(item):
    overwrite_titlecase = {}
    if str(item.title).lower() == '[]':
        return ''
    if str(item.title).lower() in overwrite_titlecase:
        return overwrite_titlecase[str(item.title).lower()]
    return str(item.title)


def directory_department(item, departments):
    if str(item.department).lower() in departments:
        return departments[str(item.department).lower()]
    return None


def disable_missing(users, webmaster):
    users.update(
        is_active=False,
        published=False,
        delete_date=timezone.now(),
        delete_user=webmaster
    )


def get_user_type(import_user):
    if str(
        import_user.userPrincipalName
    ).lower() == 'webmaster@slcschools.org':
        return 'SVC'
    elif (
        str(import_user.extensionAttribute1).startswith('E-') or
        str(import_user.extensionAttribute1).startswith('T-')
    ):
        return 'EMP'
    elif str(import_user.extensionAttribute1).startswith('N-'):
        return 'NEMP'
    else:
        return 'GST'


def importUser(import_user, webmaster):
    try:
        has_upn = User.objects.get(
            username=str(import_user.userPrincipalName).lower()
        )
    except User.DoesNotExist:
        has_upn = False
    except User.MultipleObjectsReturned:
        # Something has gone wrong with the user state for the import user.
        # Automatic conflict resolution may be able to solve this.
        import_errors.append('{0}: Duplicate username on lookup.'.format(
            str(import_user.userPrincipalName).lower()
        ))
        return False
    try:
        has_sync = User.objects.get(
            sync_uuid=uuid.UUID(str(import_user.objectGUID))
        )
    except User.DoesNotExist:
        has_sync = False
    except User.MultipleObjectsReturned:
        # Something has gone wrong with the user state for the import user.
        # Automatic conflict resolution may be able to solve this.
        import_errors.append('{0}: Duplicate sync_uuid on lookup.'.format(
            str(import_user.userPrincipalName).lower()
        ))
        return False
    user_type = get_user_type(import_user)
    if not has_upn and not has_sync:
        # Assume the user is safe to create.
        try:
            user, create = User.objects.get_or_create(
                username=str(import_user.userPrincipalName).lower(),
                sync_uuid=uuid.UUID(str(import_user.objectGUID)),
                defaults={
                    'first_name': import_user.givenName or '',
                    'last_name': import_user.sn or '',
                    'email': str(
                        import_user.mail or '').lower(),
                    'is_staff': True,
                    'is_active': True,
                    'is_superuser': False,
                    'management': False,
                    'user_type': user_type,
                    'create_user': webmaster,
                    'update_user': webmaster,
                }
            )
        except ValidationError as error:
            import_errors.append('{0}: {1}'.format(
                import_user.userPrincipalName, error
            ))
            return False
    else:
        if has_upn and not has_sync:
            # Assume the user was created manually but is still related to the
            # import user by setting the sync uuid on the has_upn user.
            user = has_upn
            user.sync_uuid = uuid.UUID(str(import_user.objectGUID))
        elif not has_upn and has_sync:
            # Assume the username has changed by using the has_sync user and
            # update the username.
            user = has_sync
            user.username = str(import_user.userPrincipalName).lower()
        elif has_upn == has_sync:
            # The import user has been imported before and is safe to work on
            # either instance of the user for updating.
            user = has_upn
        elif has_upn != has_sync:
            # Something has gone wrong with the user state for the import user.
            # Automatic conflict resolution may be able to solve this.
            import_errors.append(
                '{0}: username and sync_uuid return different users.'.format(
                    str(import_user.userPrincipalName).lower()
                )
            )
            return False
        user.first_name = import_user.givenName or ''
        user.last_name = import_user.sn or ''
        user.email = str(import_user.mail or '').lower()
        user.is_active = True
        user.user_type = user_type
        user.published = True
        user.update_user = webmaster
        user.delete_date = None
        user.delete_user = None
        try:
            user.save()
        except ValidationError as error:
            import_errors.append('{0}: {1}'.format(
                import_user.userPrincipalName, error
            ))
            return False
    return True


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(
            sync_uuid__isnull=False,
            is_active=True,
            published=True,
            delete_date__isnull=True,
            delete_user__isnull=True,
        )
        webmaster = User.objects.get(management=True)
        server = Server('slcsd.net', use_ssl=True, get_info=ALL)
        conn = Connection(
            server,
            user=get_secret('SLCSD_LDAP_USER'),
            password=get_secret('SLCSD_LDAP_PASSWORD'),
            authentication=NTLM
        )
        conn.bind()
        ldap_entries = []
        conn.search(
            'OU=DO,DC=SLCSD,DC=NET',
            '(&(!(objectClass=computer))(objectClass=person)'
            '(|(extensionAttribute1=E-*)(extensionAttribute1=T-*)'
            '(extensionAttribute1=N-*)))',
            attributes=[
                'DisplayName',
                'userPrincipalName',
                'givenName',
                'sn',
                'objectGUID',
                'mail',
                'department',
                'title',
                'extensionAttribute1',
                'memberOf',
            ],
        )
        ldap_entries += conn.entries
        conn.search(
            'OU=INFORMATION_SYSTEMS,DC=SLCSD,DC=NET',
            '(&(!(objectClass=computer))(objectClass=person)'
            '(|(extensionAttribute1=E-*)(extensionAttribute1=T-*)'
            '(extensionAttribute1=N-*)))',
            attributes=[
                'DisplayName',
                'userPrincipalName',
                'givenName',
                'sn',
                'objectGUID',
                'mail',
                'department',
                'title',
                'extensionAttribute1',
                'memberOf',
            ],
        )
        ldap_entries += conn.entries
        conn.search(
            'OU=WEB,OU=SERVERS,DC=SLCSD,DC=NET',
            '(&(!(objectClass=computer))(objectClass=person)'
            '(userPrincipalName=webmaster@SLCSCHOOLS.ORG))',
            attributes=[
                'DisplayName',
                'userPrincipalName',
                'givenName',
                'sn',
                'objectGUID',
                'mail',
                'department',
                'title',
                'extensionAttribute1',
                'memberOf',
            ],
        )
        ldap_entries += conn.entries
        processed_users = []
        for import_user in ldap_entries:
            importUser(
                import_user,
                webmaster
            )
            processed_users.append(str(import_user.objectGUID))
        users = users.exclude(sync_uuid__in=processed_users)
        disable_missing(users, webmaster)
        import_errors.sort()
        print('\n'.join(import_errors))
