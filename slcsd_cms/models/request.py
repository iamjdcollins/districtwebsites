from uuid import uuid4

from django.db import models

from .abstract import BaseModelMixin

class RequestManager(models.Manager):
    use_in_migrations = True

    def get_published(self):
        """
        Returns domains that have not been deleted and are published.

        :return:
        """
        return self.get_active().filter(published=True)

    def get_active(self):
        """
        Returns domains that have not been deleted.

        :return:
        """
        return self.get_queryset().filter(delete_date__isnull=True)


class Request(BaseModelMixin):

    scheme = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    host = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    path = models.TextField(
        null=True,
        blank=False,
    )
    method = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    encoding = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    request_content_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    request_content_length = models.BigIntegerField(
        null=True,
        blank=True,
    )
    secure = models.BooleanField(
        default=False,
    )
    ajax = models.BooleanField(
        default=False,
    )
    remote_address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    status_code = models.IntegerField(
        null=True,
        blank=True,
    )
    accept = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    user_agent  = models.TextField(
        null=True,
        blank=True,
    )
    cache_control = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    accept_language = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    connection = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    accept_encoding = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    referer = models.TextField(
        null=True,
        blank=True,
    )
    remaining_request_headers = models.TextField(
        null=True,
        blank=True,
    )
    response_content_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    response_content_length = models.BigIntegerField(
        null=True,
        blank=True,
    )
    response_vary = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    response_x_frame_options = models.TextField(
        null=True,
        blank=True,
    )
    remaining_response_headers = models.TextField(
        null=True,
        blank=True,
    )
    processing_time = models.IntegerField(
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        'slcsd_cms.Site',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='requests',
    )
    user = models.ForeignKey(
        'slcsd_cms.User',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='requests',
    )
    session = models.CharField(
        null=True,
        blank=True,
        max_length=40,
    )

    class Meta:
        get_latest_by = 'create_date'
        ordering = ('create_date', )
        verbose_name = 'request'
        verbose_name_plural = 'requests'

    def __str__(self):
        return '{0} - {1}://{2}{3}'.format(
            self.pk,
            self.scheme,
            self.host,
            self.path,
        )
