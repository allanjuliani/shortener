from unittest import mock

from django.contrib.gis.geoip2 import GeoIP2
from django.test import RequestFactory, TestCase

from apps.shortener.models import Shortener
from apps.shortener.utils import (
    generate_shortened_code,
    get_ip_info,
    random_generator,
)


class TestShortenerAdmin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_random_generator(self):
        with mock.patch(
            'random.choice',
            return_value='A',
        ):
            self.assertEqual(random_generator(), "AAAAA")

    def test_generate_shortened_code(self):
        with mock.patch(
            'apps.shortener.utils.random_generator',
            return_value='ABCDE',
        ):
            self.assertEqual(generate_shortened_code(), "ABCDE")

    def test_generate_shortened_code_one_existent(self):
        Shortener.objects.create(url='http://localhost', shortened='SKIP')
        with mock.patch(
            'apps.shortener.utils.random_generator',
            side_effect=['SKIP', 'SHORT'],
        ):
            self.assertEqual(generate_shortened_code(), "SHORT")

    def test_get_ip_info(self):
        with mock.patch.object(
            GeoIP2, '__init__', return_value=None
        ), mock.patch.object(
            GeoIP2,
            'city',
            return_value={
                'latitude': 123456789,
                'longitude': 987654321,
                'city': 'New City',
                'region': 'NC',
                'country_name': 'New Country',
            },
        ):
            request = self.factory.get('SHORT')
            self.assertEqual(
                get_ip_info(request),
                {
                    'latitude': '12345678',
                    'longitude': '98765432',
                    'city': 'New City',
                    'state': 'NC',
                    'country': 'New Country',
                },
            )
