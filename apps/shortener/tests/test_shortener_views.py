from django.http.response import Http404
from django.test import RequestFactory, TestCase

from apps.shortener.models import Shortener

from ..views import RedirectToShortenedView


class TestShortenerViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Shortener.objects.create(shortened='SHORT', url='http://localhost')

    def test_redirect_to_shortened_code(self):
        request = self.factory.get('SHORT')
        kwargs = {'code': 'SHORT'}
        response = RedirectToShortenedView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_do_not_redirect_to_shortened_invalid(self):

        request = self.factory.get('FAKE')
        kwargs = {'code': 'FAKE'}

        with self.assertRaises(Http404):
            RedirectToShortenedView.as_view()(request, **kwargs)
