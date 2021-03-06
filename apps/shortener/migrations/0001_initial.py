import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Shortener',
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
                ('url', models.URLField(unique=True, verbose_name='URL')),
                (
                    'shortened',
                    models.CharField(
                        blank=True,
                        max_length=5,
                        unique=True,
                        verbose_name='Shortened',
                    ),
                ),
                (
                    'clicks',
                    models.IntegerField(default=0, verbose_name='Clicks'),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Created at'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True, verbose_name='Updated at'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Shortener',
                'verbose_name_plural': 'Shorteners',
                'db_table': 'shortener',
            },
        ),
        migrations.CreateModel(
            name='Click',
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
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                (
                    'user_agent',
                    models.CharField(
                        blank=True,
                        max_length=512,
                        null=True,
                        verbose_name='User Agent',
                    ),
                ),
                (
                    'browser',
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name='Browser',
                    ),
                ),
                (
                    'os',
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name='OS'
                    ),
                ),
                (
                    'latitude',
                    models.CharField(
                        blank=True,
                        max_length=8,
                        null=True,
                        verbose_name='Latitude',
                    ),
                ),
                (
                    'longitude',
                    models.CharField(
                        blank=True,
                        max_length=8,
                        null=True,
                        verbose_name='Longitude',
                    ),
                ),
                (
                    'city',
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name='City',
                    ),
                ),
                (
                    'state',
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name='State',
                    ),
                ),
                (
                    'country',
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name='Country',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Created at'
                    ),
                ),
                (
                    'shortener',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='shortener.shortener',
                        verbose_name='Shortener',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Click',
                'verbose_name_plural': 'Clicks',
                'db_table': 'shortener_click',
            },
        ),
    ]
