from uuid import uuid4

from django.db import models
from django.contrib.auth.models import Group

Group.add_to_class('uuid',  models.UUIDField(
    unique=True,
    default=uuid4,
    editable=False,
))
Group.add_to_class('title', models.CharField(
    null=True,
    blank=False,
    max_length=250,
    verbose_name='Site Title',
))
Group.add_to_class('description', models.TextField(
    null=True,
    blank=True,
    verbose_name='Description',
))
