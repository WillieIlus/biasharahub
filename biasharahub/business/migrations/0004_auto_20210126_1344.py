# Generated by Django 2.2.12 on 2021-01-26 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20210105_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='company', to='categories.Category'),
        ),
    ]
