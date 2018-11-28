from django.conf import settings
from django.db import models

from .abstract import BaseModelMixin


class DomainManager(models.Manager):
    use_in_migrations = True

    def get_published(self):
        return self.get_active().filter(published=True)

    def get_active(self):
        return self.get_queryset().filter(delete_date__isnull=True)

    def get_canonical(self, environment=settings.ENVIRONMENT):
        try:
            canonical = self.get_published().get(
                site=self.instance,
                environment=environment,
                canonical=True,
            )
        except Domain.DoesNotExist:
            domains = self.get_published().filter(
                site=self.instance,
                environment=environment
            )
            if len(domains) > 0:
                canonical = domains[0]
                canonical._meta.model.objects.filter(
                    pk=canonical.pk).update(canonical=True)
            else:
                canonical = None
        return canonical


class Domain(BaseModelMixin):

    ENVIRONMENTS = (
        ('DEVELOPMENT', 'Development'),
        ('TESTING', 'Testing'),
        ('PRODUCTION', 'Production'),
    )

    domain = models.CharField(
        db_index=True,
        null=False,
        blank=False,
        max_length=200,
        verbose_name='Domain Name',
    )
    site = models.ForeignKey(
        'slcsd_cms.Site',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='domains',
    )
    environment = models.CharField(
        null=False,
        blank=False,
        max_length=12,
        verbose_name='Environment',
        choices=ENVIRONMENTS
    )
    canonical = models.BooleanField(
        default=False,
        db_index=True,
    )

    objects = DomainManager()

    class Meta:
        get_latest_by = 'create_date'
        ordering = ('domain', )
        verbose_name = 'domain'
        verbose_name_plural = 'domains'

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        # Run full clean to make sure that all inputs are valid. Without this the save method does not run all
        # validations. I would rather validations run multiple times than not at all.
        self.full_clean()
        # A domain that is not published or has been deleted cannot also be canonical.
        if not self.published or self.delete_date:
            self.canonical = False
        # Set all domains with the same site and environment to not canonical if the current domain has been set as
        # canonical but was not before save.
        if self.canonical:
            self._meta.model.objects.filter(
                site=self.site,
                environment=self.environment
            ).update(canonical=False)
            self._meta.model.objects.filter(
                pk=self.pk).update(canonical=True)
        # Run the save from the inherited model
        super(self._meta.model, self).save(*args, **kwargs)
        # Sync up canonical attributes.
        if self.canonical:
            self.site.set_canonical(self.environment, self)
        else:
            self.site.unset_canonical(self.environment, self)
        # Rebuild the site > domain cache.
        self.site._meta.model.objects.rebuild_cache()
