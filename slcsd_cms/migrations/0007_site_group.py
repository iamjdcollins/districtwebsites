# Generated by Django 2.1.2 on 2018-12-04 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('slcsd_cms', '0006_remove_site_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='group',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='site', to='auth.Group', to_field='uuid'),
        ),
    ]
