# Generated by Django 2.2.12 on 2021-01-26 10:44

from django.db import migrations, models
import utility.models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20210105_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_author',
            field=models.CharField(blank=True, max_length=255, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_copyright',
            field=models.CharField(blank=True, max_length=255, verbose_name='Copyright'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=utility.models.TruncatingCharField(blank=True, max_length=255, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(blank=True, help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords'),
        ),
    ]
