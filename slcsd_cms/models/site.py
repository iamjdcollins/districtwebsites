from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.db import models
from django.http import Http404
from django.http.request import split_domain_port
from django.shortcuts import redirect

from .abstract import BaseModelMixin
from .domain import Domain


class SiteManager(models.Manager):
    use_in_migrations = True

    def get_published(self):
        return self.get_active().filter(published=True)

    def get_active(self):
        return self.get_queryset().filter(delete_date__isnull=True)

    def _get_site_by_request(self, request):
        SLCSD_CMS_SITES = cache.get('SLCSD_CMS_SITES')
        if not SLCSD_CMS_SITES:
            SLCSD_CMS_SITES = self.rebuild_cache()
        domain, port = split_domain_port(request.get_host())
        if domain not in SLCSD_CMS_SITES:
            raise Http404()
        if SLCSD_CMS_SITES[domain]['canonical']:
            canonical_domain = SLCSD_CMS_SITES[domain]['canonical'].domain
            if domain != canonical_domain:
                return redirect(
                    'https://{0}{1}'.format(
                        canonical_domain,
                        request.path
                    ),
                    permanent=True
                )
        else:
            raise Http404()
        return SLCSD_CMS_SITES[domain]['site']

    def get_current(self, request=None):
        """
        Return the current Site based on the SITE_ID in the project's settings.
        If SITE_ID isn't defined, return the site with domain matching
        request.get_host(). The ``Site`` object is cached the first time it's
        retrieved from the database.
        """
        return self._get_site_by_request(request)

    def rebuild_cache(self):
        SLCSD_CMS_SITES = {}
        for domain in Domain.objects.filter(
            environment=settings.ENVIRONMENT
        ):
            SLCSD_CMS_SITES[domain.domain] = {
                'site': domain.site,
                'canonical': domain.site.get_canonical,
            }
        cache.set('SLCSD_CMS_SITES', SLCSD_CMS_SITES, None)
        return SLCSD_CMS_SITES


class Site(BaseModelMixin):

    title = models.CharField(
        null=False,
        blank=False,
        max_length=200,
        verbose_name='Site Title',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Description',
    )
    management = models.BooleanField(
        default=False,
        db_index=True,
    )
    group = models.OneToOneField(
        Group,
        null=True,
        blank=False,
        editable=False,
        unique=True,
        on_delete=models.PROTECT,
        related_name='site',
    )

    objects = SiteManager()

    class Meta:
        get_latest_by = 'create_date'
        ordering = ('title', )
        verbose_name = 'site'
        verbose_name_plural = 'sites'

    def __str__(self):
        return self.title

    @property
    def get_canonical(self):
        return self.domains.get_canonical()

    @property
    def development_canonical(self):
        return self.domains.get_canonical(environment='DEVELOPMENT')

    @property
    def testing_canonical(self):
        return self.domains.get_canonical(environment='TESTING')

    @property
    def production_canonical(self):
        return self.domains.get_canonical(environment='PRODUCTION')

    def create_group(self):
        group_type = 'Publishers' if not self.management else 'Managers'
        self.group, created = Group.objects.get_or_create(
            name='{0}'.format(self.pk),
            defaults={
                'title': '{0} {1}'.format(
                    self.title,
                    group_type,
                ),
                'description': '{0} group for site: {1}'.format(
                    group_type,
                    self.title,
                )
            }
        )
        if not created:
            self.group.title = '{0} {1}'.format(self.title, group_type)
            self.group.description = '{0} group for site: {1}'.format(
                group_type,
                self.title,
            )
            self.group.save()
        return self.group

    def save(self, *args, **kwargs):
        self.full_clean()
        self.create_group()
        # Run the save from the inherited model
        super(self._meta.model, self).save(*args, **kwargs)
