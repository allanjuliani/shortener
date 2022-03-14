from django.conf import settings
from django.test import TestCase

from apps.shortener.admin import LogAdmin, ShortenerAdmin
from apps.shortener.models import Log, Shortener


class TestShortenerAdmin(TestCase):
    def setUp(self):
        self.shortenerAdmin = ShortenerAdmin
        self.logAdmin = LogAdmin
        self.shortener = Shortener.objects.create(
            url='http://localhost', shortened='SHORT'
        )
        self.log = Log.objects.create(
            shortener=self.shortener, ip='127.0.0.1', latitude=1, longitude=1
        )

    def test_get_exclude(self):
        self.assertEqual(
            self.shortenerAdmin.get_exclude(self=None, request=None, obj=None),
            ('clicks_link',),
        )
        self.assertEqual(
            self.shortenerAdmin.get_exclude(
                self=None, request=None, obj=self.shortener
            ),
            ([],),
        )

    def test_get_readonly_fields(self):
        self.assertEqual(
            self.shortenerAdmin.get_readonly_fields(
                self=None, request=None, obj=None
            ),
            [],
        )
        self.assertEqual(
            self.shortenerAdmin.get_readonly_fields(
                self=None, request=None, obj=self.shortener
            ),
            [
                'id',
                'url',
                'shortened_link',
                'clicks_link',
                'created_at',
                'updated_at',
            ],
        )

    def test_get_fields(self):
        self.assertEqual(
            self.shortenerAdmin.get_fields(self=None, request=None, obj=None),
            ['url', 'shortened'],
        )
        self.assertEqual(
            self.shortenerAdmin.get_fields(
                self=None, request=None, obj=self.shortener
            ),
            [
                'id',
                'url',
                'shortened_link',
                'clicks_link',
                'created_at',
                'updated_at',
            ],
        )

    def test_shortened_link(self):
        self.assertEqual(
            self.shortenerAdmin.shortened_link(self=None, obj=self.shortener),
            f'{settings.DOMAIN}SHORT&nbsp;<a target="_blank" '
            f'class="viewlink" href="{settings.DOMAIN}SHORT"></a>',
        )

    def test_clicks_link(self):
        self.assertEqual(
            self.shortenerAdmin.clicks_link(self=None, obj=self.shortener),
            '<a href="/admin/shortener/log/?shortener__id__exact=1">0</a>',
        )

    def test_google_maps(self):
        self.assertEqual(
            self.logAdmin.google_maps(self=None, obj=self.log),
            '<iframe class="map" width="240" height="180" '
            'frameborder="0" scrolling="no" marginheight="0" '
            'marginwidth="0" '
            'src="https://maps.google.com/?ll=1,1&z=11&output=embed">'
            '</iframe>',
        )

    def test_view_shortener(self):
        self.assertEqual(
            self.logAdmin.view_shortener(self=None, obj=self.log),
            '<a href="/admin/shortener/shortener/1/change/">SHORT</a>',
        )
