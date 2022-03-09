from unittest import mock

from django.test import TestCase

from apps.shortener.models import Shortener


class TestShortenerModels(TestCase):
    model = Shortener

    def test_shortened_str(self):
        shortener = self.model.objects.create(
            url='http://localhost', shortened='SHORT'
        )
        self.assertEqual(str(shortener), 'SHORT')

    def test_random_shortened_str(self):
        with mock.patch(
            'apps.shortener.models.generate_shortened_code',
            return_value='VALUE',
        ):
            shortener = self.model.objects.create(
                url='http://localhost',
            )
            self.assertEqual(str(shortener), 'VALUE')
