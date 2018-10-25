from django.db import models
from django.contrib.auth.models import Group

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
