# Generated by Django 2.2.1 on 2019-05-26 08:29

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20190526_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=authentication.models.custom_upload_url),
        ),
    ]