# Generated by Django 2.2.12 on 2020-10-19 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('icon', models.CharField(max_length=50, unique=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country', to='locations.Country')),
            ],
            options={
                'verbose_name_plural': 'locations',
                'ordering': ['name'],
            },
        ),
    ]
