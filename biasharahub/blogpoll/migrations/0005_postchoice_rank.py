# Generated by Django 2.2.12 on 2021-02-19 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpoll', '0004_auto_20210219_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='postchoice',
            name='rank',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
