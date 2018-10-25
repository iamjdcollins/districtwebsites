from django.core.management.base import (
    BaseCommand,
)

from slcsd_cms.models import (
    User,
    Site,
    Domain,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            management_user = User.objects.get(management=True)
        except User.DoesNotExist:
            management_user = False
        try:
            management_site = Site.objects.get(management=True)
        except Site.DoesNotExist:
            management_site = False
        if not management_user and not management_site:
            username = input(
                'Enter the management account username (should be an email '
                'address): '
            )
            production = input(
                'Enter the production domain for the management site: '
            )
            testing = input(
                'Enter the testing domain for the management site: '
            )
            development = input(
                'Enter the development domain for the management site: '
            )
            user, created = User.objects.get_or_create(
                username=str(username).lower(),
                defaults={
                    'first_name': 'Webmaster',
                    'last_name': 'Account',
                    'email': str(username).lower(),
                    'is_active': True,
                    'is_staff': True,
                    'is_superuser': True,
                    'user_type': 'SVC',
                    'management': True,
                }
            )
            site, created = Site.objects.get_or_create(
                title='Management Website',
                defaults={
                    'description': 'The management website.',
                    'management': True,
                }
            )
            production, create = Domain.objects.get_or_create(
                domain=production,
                defaults={
                    'site': site,
                    'canonical': True,
                    'environment': 'PRODUCTION',
                }
            )
            testing, create = Domain.objects.get_or_create(
                domain=testing,
                defaults={
                    'site': site,
                    'canonical': True,
                    'environment': 'TESTING',
                }
            )
            development, create = Domain.objects.get_or_create(
                domain=development,
                defaults={
                    'site': site,
                    'canonical': True,
                    'environment': 'DEVELOPMENT',
                }
            )
        else:
            print('The cms appears to have already been initialized.')
