# Generated by Django 4.0.1 on 2022-01-18 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='covidstatistics',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='states',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='country',
            table='country',
        ),
        migrations.AlterModelTable(
            name='covidstatistics',
            table='covid_statistics',
        ),
        migrations.AlterModelTable(
            name='states',
            table='states',
        ),
    ]
