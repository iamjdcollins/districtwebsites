from uuid import uuid4

from django.conf import settings
from django.db import models


class BaseModelMixin(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False,
    )
    published = models.BooleanField(
        default=True,
        db_index=True,
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_create_user',
    )
    update_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_update_user',
    )
    delete_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )
    delete_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_delete_user',
    )

    class Meta:
        abstract = True
