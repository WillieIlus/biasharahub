# Generated by Django 2.2.12 on 2020-12-20 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_auto_20201115_1526'),
        ('openinghours', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghours',
            options={'ordering': ['company', 'weekday', 'from_hour'], 'verbose_name': 'Opening Hours', 'verbose_name_plural': 'Opening Hours'},
        ),
        migrations.RenameField(
            model_name='openinghours',
            old_name='start',
            new_name='from_hour',
        ),
        migrations.RenameField(
            model_name='openinghours',
            old_name='end',
            new_name='to_hour',
        ),
        migrations.CreateModel(
            name='ClosingRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='Start')),
                ('end', models.DateTimeField(verbose_name='End')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='Reason')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='closing_rules', to='business.Business', verbose_name='company')),
            ],
            options={
                'verbose_name': 'Closing Rule',
                'verbose_name_plural': 'Closing Rules',
                'ordering': ['start'],
            },
        ),
    ]
