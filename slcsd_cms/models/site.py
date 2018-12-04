from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import Http404
from django.http.request import split_domain_port
from django.shortcuts import redirect

from .abstract import BaseModelMixin
from .domain import Domain


class SiteManager(models.Manager):
    use_in_migrations = True

    def get_published(self):
        """
        Returns sites that have not be deleted and are published.

        :return:
        """
        return self.get_active().filter(published=True)

    def get_active(self):
        """
        Returns sites that have not be deleted.

        :return:
        """
        return self.get_queryset().filter(delete_date__isnull=True)

    def _get_site_by_request(self, request):
        """
        Returns the current site from the SLCSD_CMS_SITES cache.

        If the cache is empty it should be rebuilt. If the domain is not
        found in the cache a 404 should be raised. If the domain is found
        but not canonical a redirect to the canonical domain should occur.
        """
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
        Return the current Site based by looking up the site in the
        SLCSD_CMS_SITES cache.
        """
        return self._get_site_by_request(request)

    def rebuild_cache(self):
        """
        Builds a cache of domains and their respective site and canonical
        domain.

        This allows for quickly determining what site a request is coming to
        and if it is accessing the canonical domain.
        :return:
        """
        SLCSD_CMS_SITES = {}
        for domain in Domain.objects.all():
            if domain.environment == 'DEVELOPMENT':
                SLCSD_CMS_SITES[domain.domain] = {
                    'site': domain.site,
                    'canonical': domain.site.development_canonical,
                }
            if domain.environment == 'TESTING':
                SLCSD_CMS_SITES[domain.domain] = {
                    'site': domain.site,
                    'canonical': domain.site.testing_canonical,
                }
            if domain.environment == 'PRODUCTION':
                SLCSD_CMS_SITES[domain.domain] = {
                    'site': domain.site,
                    'canonical': domain.site.production_canonical,
                }
        cache.set('SLCSD_CMS_SITES', SLCSD_CMS_SITES, None)
        return SLCSD_CMS_SITES


class Site(BaseModelMixin):
    """
    Represents a single websites.
    """
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
        to_field='uuid',
        related_name='site',
    )
    development_canonical = models.OneToOneField(
        Domain,
        null=True,
        blank=True,
        editable=False,
        unique=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    testing_canonical = models.OneToOneField(
        Domain,
        null=True,
        blank=True,
        editable=False,
        unique=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    production_canonical = models.OneToOneField(
        Domain,
        null=True,
        blank=True,
        editable=False,
        unique=True,
        on_delete=models.SET_NULL,
        related_name='+',
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
    def canonical(self):
        """
        Returns the current canonical domain for the site.

        Based on the current running environment return the canonical domain
        for the site. If there is not a canonical domain for the current
        environment and site return None.
        """
        if settings.ENVIRONMENT == 'DEVELOPMENT':
            return self.development_canonical
        elif settings.ENVIRONMENT == 'TESTING':
            return self.testing_canonical
        elif settings.ENVIRONMENT == 'PRODUCTION':
            return self.production_canonical
        return None

    @property
    def canonical_id(self):
        """
        Returns the current canonical domains primary key.

        Based on the current running environment return the canonical domains
        primary key for the site. If there is not a canonical domain for the
        current environment and site return None.
        """
        if settings.ENVIRONMENT == 'DEVELOPMENT':
            return self.development_canonical_id
        elif settings.ENVIRONMENT == 'TESTING':
            return self.testing_canonical_id
        elif settings.ENVIRONMENT == 'PRODUCTION':
            return self.production_canonical_id
        return None

    def set_canonical(self, environment, domain):
        """
        Sets the domain for a given environment as canonical on the site.

        This method should set the passed in domain as the canonical domain
        for the given environment. If the domain is already set the method
        should not make or save any changes.

        :param environment:
        :param domain:
        """
        changed = False
        if environment == 'DEVELOPMENT' and self.development_canonical != \
                domain:
            self.development_canonical = domain
            changed = True
        elif environment == 'TESTING' and self.testing_canonical != domain:
            self.testing_canonical = domain
            changed = True
        elif environment == 'PRODUCTION' and self.production_canonical != \
                domain:
            self.production_canonical = domain
            changed = True
        if changed:
            self.save()

    def unset_canonical(self, environment, domain):
        """
        Removes the domain for a given environment as the canonical of the
        site.

        This method should remove the passed in domain as the canonical
        domain for the given environment. If the domain is not currently set
        as the canonical domain the method should not make or save any changes.

        :param environment:
        :param domain:
        """
        changed = False
        if environment == 'DEVELOPMENT' and self.development_canonical == \
                domain:
            self.development_canonical = None
            changed = True
        elif environment == 'TESTING' and self.testing_canonical == domain:
            self.testing_canonical = None
            changed = True
        elif environment == 'PRODUCTION' and self.production_canonical == \
                domain:
            self.production_canonical = None
            changed = True
        if changed:
            self.save()

    def create_group(self):
        """
        Creates a publisher or manager group that is associated with the site.

        This method should create a group that represents the managers or
        publishers associated with the given site. If the group was already
        created we need to check if the current title and description need
        to be updated and write the changes only if needed.

        :return:
        """
        group_type = 'Publishers' if not self.management else 'Managers'
        group_title = '{0} {1}'.format(self.title, group_type)
        group_description = '{0} group for site: {1}'.format(
            group_type,
            self.title
        )
        self.group, created = Group.objects.get_or_create(
            name='{0}'.format(self.pk),
            defaults={
                'title': group_title,
                'description': group_description
            }
        )
        if not created:
            original_group = {
                'title': self.group.title,
                'description': self.group.description,
            }
            new_group = {
                'title': group_title,
                'description': group_description,
            }
            if original_group != new_group:
                self.group.title = group_title
                self.group.description = group_description
                self.group.save()
        return self.group

    def save(self, *args, **kwargs):
        self.full_clean()
        self.create_group()
        # Run the save from the inherited model
        super(self._meta.model, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.management:
            raise PermissionDenied(
                'You cannot delete the management website. First create a '
                'new management website.'
            )
        super(self._meta.model, self).delete(*args, **kwargs)
        # After deleting the site you should delete the related group. This
        # is required because the group relation does not point back to the
        # site like other models but instead this model had to point to the
        # group.
        if self.group:
            self.group.delete()
