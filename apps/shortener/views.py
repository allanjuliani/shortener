from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .utils import create_access_log, get_shortener


class RedirectToShortenedView(TemplateView):
    def get(self, request, code):
        shortener = get_shortener(code)

        if shortener:
            create_access_log(request, shortener)

            return redirect(shortener.url)
        else:
            raise Http404
