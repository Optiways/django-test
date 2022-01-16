# Generated by Django 3.2.5 on 2022-01-16 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0001_initial'),
        ('fleet', '0002_auto_20211109_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='Time')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.place', verbose_name='Place')),
            ],
            options={
                'verbose_name': 'Bus stop',
                'verbose_name_plural': 'Bus stops',
                'ordering': ['time'],
            },
        ),
        migrations.CreateModel(
            name='BusShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_dt', models.DateTimeField(verbose_name='Beginning of the trip')),
                ('end_dt', models.DateTimeField(verbose_name='End of the trip')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.bus', verbose_name='Bus')),
                ('bus_stop', models.ManyToManyField(to='fleet.BusStop')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.driver', verbose_name='Driver')),
            ],
            options={
                'verbose_name': 'Bus shift',
                'verbose_name_plural': 'Bus shifts',
            },
        ),
    ]