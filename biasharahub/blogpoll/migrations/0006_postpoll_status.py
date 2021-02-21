# Generated by Django 2.2.12 on 2021-02-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpoll', '0005_postchoice_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpoll',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
