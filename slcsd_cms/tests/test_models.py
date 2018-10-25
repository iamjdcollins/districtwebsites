from uuid import uuid4

from django.conf.global_settings import CACHES
from django.db import IntegrityError
from django.test import TestCase, RequestFactory, override_settings
from django.utils import timezone

from ..models import (
    User,
    Site,
    Domain,
)


def create_webmaster():

    webmaster, created = User.objects.get_or_create(
        username='webmaster@slcschools.org',
        defaults={
            'uuid': uuid4(),
            'first_name': 'Webmaster',
            'last_name': 'Account',
            'email': 'webmaster@slcschools.org',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True,
            'user_type': 'SVC',
            'date_joined': timezone.now(),
            'published': True,
            'create_date': timezone.now(),
            'create_user': None,
            'update_date': timezone.now(),
            'update_user': None,
            'delete_date': None,
            'delete_user': None,
        }
    )
    return webmaster


def create_management_website(webmaster):
    management, created = Site.objects.get_or_create(
        title='Management Website',
        defaults={
            'uuid': uuid4(),
            'title': 'Management Website',
            'description': 'The management website.',
            'management': True,
            'published': True,
            'create_date': timezone.now(),
            'create_user': webmaster,
            'update_date': timezone.now(),
            'update_user': webmaster,
            'delete_date': None,
            'delete_user': None,
        }
    )
    return management


class UserTestCase(TestCase):

    def setUp(self):
        webmaster = create_webmaster()
        deleted, created = User.objects.get_or_create(
            username='deleted@slcschools.org',
            defaults={
                'uuid': uuid4(),
                'first_name': 'Deleted',
                'last_name': 'Account',
                'email': 'deleted@slcschools.org',
                'is_staff': True,
                'is_active': True,
                'user_type': 'EMP',
                'date_joined': timezone.now(),
                'published': True,
                'create_date': timezone.now(),
                'create_user': None,
                'update_date': timezone.now(),
                'update_user': None,
                'delete_date': timezone.now(),
                'delete_user': webmaster,
            }
        )
        unpublished, created = User.objects.get_or_create(
            username='unpublished@slcschools.org',
            defaults={
                'uuid': uuid4(),
                'first_name': 'Unpublished',
                'last_name': 'Account',
                'email': 'unpublished@slcschools.org',
                'is_staff': True,
                'is_active': False,
                'user_type': 'EMP',
                'date_joined': timezone.now(),
                'published': False,
                'create_date': timezone.now(),
                'create_user': None,
                'update_date': timezone.now(),
                'update_user': None,
                'delete_date': None,
                'delete_user': None,
            }
        )

    def test_webmaster(self):
        user = User.objects.get(
            username='webmaster@slcschools.org'
        )
        user.clean()

        self.assertEquals(
            1,
            len(
                User.objects.filter(username='webmaster@slcschools.org')
            )
        )
        self.assertEquals(
            'Webmaster Account',
            user.get_full_name()
        )
        self.assertEquals(
            'Webmaster',
            user.get_short_name()
        )
        self.assertEquals(
            'webmaster@slcschools.org',
            user.email
        )
        self.assertEquals(
            1,
            user.email_user(
                subject='Test',
                message='Test',
                from_email='test@slcschools.org',
            )
        )
        user.email = None
        self.assertEquals(
            0,
            user.email_user(
                subject='Test',
                message='Test',
                from_email='test@slcschools.org',
            )
        )

    def test_all_accounts_len(self):
        self.assertEquals(
            3,
            len(User.objects.all())
        )

    def test_published_accounts_len(self):
        self.assertEquals(
            1,
            len(User.objects.get_published())
        )

    def test_active_accounts_len(self):
        self.assertEquals(
            2,
            len(User.objects.get_active())
        )

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username=None)

    def test_create_user_with_username(self):
        user = User.objects.create_user(
            username='shouldcreate@slcschools.org'
        )
        self.assertIsInstance(user, User)

    def test_create_superuser_without_args(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser()

    def test_create_superuser_without_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='supershouldcreate@slcschools.org',
                email='supershouldcreate@slcschools.org',
                password='Abc123',
                is_staff=False,
            )

    def test_create_superuser_without_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='supershouldcreate@slcschools.org',
                email='supershouldcreate@slcschools.org',
                password='Abc123',
                is_superuser=False,
            )

    def test_create_superuser_with_agrs(self):
        user = User.objects.create_superuser(
            username='supershouldcreate@slcschools.org',
            email='supershouldcreate@slcschools.org',
            password='Abc123'
        )
        self.assertIsInstance(user, User)

    def test_create_user_existing(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='webmaster@slcschools.org'
            )


class SiteTestCase(TestCase):

    def setUp(self):
        webmaster = create_webmaster()
        create_management_website(webmaster)
        deleted, created = Site.objects.get_or_create(
            uuid=uuid4(),
            defaults={
                'title': 'Deleted Site',
                'description': '',
                'management': False,
                'published': True,
                'create_date': timezone.now(),
                'create_user': webmaster,
                'update_date': timezone.now(),
                'update_user': webmaster,
                'delete_date': timezone.now(),
                'delete_user': webmaster,
            }
        )
        unpublished, created = Site.objects.get_or_create(
            uuid=uuid4(),
            defaults={
                'title': 'Unpublished Website',
                'description': '',
                'management': False,
                'published': False,
                'create_date': timezone.now(),
                'create_user': webmaster,
                'update_date': timezone.now(),
                'update_user': webmaster,
                'delete_date': None,
                'delete_user': None,
            }
        )

    def test_management_site(self):
        management = Site.objects.get(management=1)
        self.assertEquals(
            1,
            len(Site.objects.filter(management=1))
        )
        self.assertEquals(
            'Management Website',
            str(management)
        )

    def test_all_sites_len(self):
        self.assertEquals(
            3,
            len(Site.objects.all())
        )

    def test_published_sites_len(self):
        self.assertEquals(
            1,
            len(Site.objects.get_published())
        )

    def test_active_sites_len(self):
        self.assertEquals(
            2,
            len(Site.objects.get_active())
        )


@override_settings(CACHES=CACHES)
class DomainTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.webmaster = create_webmaster()
        self.management = create_management_website(self.webmaster)

        development_canonical, created = Domain.objects.get_or_create(
            domain='websites-dev.slcschools.org',
            defaults={
                'uuid': uuid4(),
                'site': self.management,
                'environment': 'DEVELOPMENT',
                'canonical': True,
                'published': True,
                'create_date': timezone.now(),
                'create_user': self.webmaster,
                'update_date': timezone.now(),
                'update_user': self.webmaster,
                'delete_date': None,
                'delete_user': None,

            }

        )
        testing_canonical, created = Domain.objects.get_or_create(
            domain='websites-test.slcschools.org',
            defaults={
                'uuid': uuid4(),
                'site': self.management,
                'environment': 'TESTING',
                'canonical': True,
                'published': True,
                'create_date': timezone.now(),
                'create_user': self.webmaster,
                'update_date': timezone.now(),
                'update_user': self.webmaster,
                'delete_date': None,
                'delete_user': None,

            }

        )
        notcanonical, created = Domain.objects.get_or_create(
            domain='notcanonical.slcschools.org',
            defaults={
                'uuid': uuid4(),
                'site': self.management,
                'environment': 'DEVELOPMENT',
                'canonical': False,
                'published': True,
                'create_date': timezone.now(),
                'create_user': self.webmaster,
                'update_date': timezone.now(),
                'update_user': self.webmaster,
                'delete_date': None,
                'delete_user': None,

            }

        )
        production_canonical, created = Domain.objects.get_or_create(
            domain='websites.slcschools.org',
            defaults={
                'uuid': uuid4(),
                'site': self.management,
                'environment': 'PRODUCTION',
                'canonical': True,
                'published': True,
                'create_date': timezone.now(),
                'create_user': self.webmaster,
                'update_date': timezone.now(),
                'update_user': self.webmaster,
                'delete_date': None,
                'delete_user': None,

            }

        )
        deleted, created = Domain.objects.get_or_create(
            domain='deleted.slcschools.org',
            defaults={
                'uuid': uuid4(),
                'site': self.management,
                'environment': 'PRODUCTION',
                'canonical': False,
                'published': True,
                'create_date': timezone.now(),
                'create_user': self.webmaster,
                'update_date': timezone.now(),
                'update_user': self.webmaster,
                'delete_date': timezone.now(),
                'delete_user': self.webmaster,

            }

        )
        unpublished, created = Domain.objects.get_or_create(
            domain='unpublished.slcschools.org',
            defaults={
                'uuid': uuid4(),
                'site': self.management,
                'environment': 'PRODUCTION',
                'canonical': False,
                'published': False,
                'create_date': timezone.now(),
                'create_user': self.webmaster,
                'update_date': timezone.now(),
                'update_user': self.webmaster,
                'delete_date': None,
                'delete_user': None,

            }

        )

    def test_all_domains_len(self):
        self.assertEquals(
            6,
            len(Domain.objects.all())
        )

    def test_published_domains_len(self):
        self.assertEquals(
            4,
            len(Domain.objects.get_published())
        )

    def test_active_domains_len(self):
        self.assertEquals(
            5,
            len(Domain.objects.get_active())
        )

    def test_site_get_canonical(self):
        webmaster = create_webmaster()
        management = create_management_website(webmaster)
        self.assertEquals(
            'websites-dev.slcschools.org',
            str(management.get_canonical())
        )

    def test_redirect_request(self):
        request = self.client.get(
            '/',
            HTTP_HOST='notcanonical.slcschools.org'
        )
        self.assertEquals(request.status_code, 301)

    def test_change_canonical(self):

        newcanonical, created = Domain.objects.get_or_create(
            domain='newcanonical.slcschools.org',
            defaults={
                'uuid': uuid4(),
                'site': self.management,
                'environment': 'DEVELOPMENT',
                'canonical': True,
                'published': True,
                'create_date': timezone.now(),
                'create_user': self.webmaster,
                'update_date': timezone.now(),
                'update_user': self.webmaster,
                'delete_date': None,
                'delete_user': None,

            }

        )
        request = self.client.get(
            '/',
            HTTP_HOST='newcanonical.slcschools.org'
        )
        self.assertNotEquals(
            request.status_code,
            301
        )

    def test_unpublish_canonical(self):
        canonical = self.management.domains.get_canonical()
        canonical.published = False
        canonical.save()
        self.assertEquals(
            'notcanonical.slcschools.org',
            self.management.domains.get_canonical().domain
        )

    def test_no_canonical(self):

        for domain in self.management.domains.filter(
            environment='DEVELOPMENT'
        ):
            domain.published = False
            domain.save()
        request = self.client.get(
            '/',
            HTTP_HOST='notcanonical.slcschools.org'
        )
        self.assertEquals(request.status_code, 404)

    def test_empty_cache_accessing_nonexisting_domain(self):
        from django.core.cache import cache
        cache.clear()
        request = self.client.get(
            '/',
            HTTP_HOST='doesnotexist.slcschools.org'
        )
        self.assertEquals(request.status_code, 404)
