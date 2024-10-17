# Generated by Django 3.2.5 on 2024-10-15 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geography', '0001_initial'),
        ('fleet', '0002_auto_20211109_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.bus')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.driver')),
            ],
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transit_time', models.DateTimeField()),
                ('bus_shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stops', to='transit.busshift')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.place')),
            ],
        ),
    ]
