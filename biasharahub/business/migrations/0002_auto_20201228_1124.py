# Generated by Django 2.2.12 on 2020-12-28 08:24

from django.db import migrations
import utility.models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='meta_description',
            field=utility.models.TruncatingCharField(blank=True, max_length=255, verbose_name='Description'),
        ),
    ]
