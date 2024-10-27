# Generated by Django 3.2.5 on 2024-10-27 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import padam_django.apps.common.fields
import padam_django.apps.common.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StartBusStop',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'ts_create',
                    padam_django.apps.common.fields.TsCreateField(
                        auto_now_add=True,
                        help_text='Date at which the object was created.',
                        verbose_name='Creation date',
                    ),
                ),
                (
                    'ts_update',
                    padam_django.apps.common.fields.TsUpdateField(
                        auto_now=True,
                        help_text='Date at which the object was updated.',
                        verbose_name='Last update date',
                    ),
                ),
                (
                    'ts_requested',
                    models.DateTimeField(
                        help_text='Requested time by the user to get picked up',
                        validators=[
                            padam_django.apps.common.validators.validate_future_date
                        ],
                        verbose_name='Requested boarding time',
                    ),
                ),
                (
                    'ts_estimated',
                    models.DateTimeField(
                        blank=True,
                        help_text='Estimated Bus arrival time by the BusShift algorithm',
                        null=True,
                        verbose_name='Estimated boarding time',
                    ),
                ),
                (
                    'ts_boarded',
                    models.DateTimeField(
                        blank=True,
                        help_text='Time when the user has been picked up by the bus',
                        null=True,
                        verbose_name='Real boarding time',
                    ),
                ),
                (
                    'has_boarded',
                    models.BooleanField(
                        default=False,
                        help_text='Checks if the user has boarded the bus',
                        verbose_name='Has Boarded',
                    ),
                ),
                (
                    'place',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='geography.place',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
                'unique_together': {('user', 'place', 'ts_requested')},
            },
        ),
        migrations.CreateModel(
            name='EndBusStop',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'ts_create',
                    padam_django.apps.common.fields.TsCreateField(
                        auto_now_add=True,
                        help_text='Date at which the object was created.',
                        verbose_name='Creation date',
                    ),
                ),
                (
                    'ts_update',
                    padam_django.apps.common.fields.TsUpdateField(
                        auto_now=True,
                        help_text='Date at which the object was updated.',
                        verbose_name='Last update date',
                    ),
                ),
                (
                    'ts_requested',
                    models.DateTimeField(
                        help_text='Requested time by the user to get picked up',
                        validators=[
                            padam_django.apps.common.validators.validate_future_date
                        ],
                        verbose_name='Requested boarding time',
                    ),
                ),
                (
                    'ts_estimated',
                    models.DateTimeField(
                        blank=True,
                        help_text='Estimated Bus arrival time by the BusShift algorithm',
                        null=True,
                        verbose_name='Estimated boarding time',
                    ),
                ),
                (
                    'ts_boarded',
                    models.DateTimeField(
                        blank=True,
                        help_text='Time when the user has been picked up by the bus',
                        null=True,
                        verbose_name='Real boarding time',
                    ),
                ),
                (
                    'has_boarded',
                    models.BooleanField(
                        default=False,
                        help_text='Checks if the user has boarded the bus',
                        verbose_name='Has Boarded',
                    ),
                ),
                (
                    'place',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='geography.place',
                    ),
                ),
                (
                    'start',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='end',
                        to='travel.startbusstop',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
