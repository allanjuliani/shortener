from django.http import Http404, HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .utils import add_new_click, create_access_log, get_shortener


class RedirectToShortenedView(TemplateView):
    def get(self, request: HttpRequest, code: str):
        shortener = get_shortener(code)

        if shortener:
            create_access_log(request, shortener)
            add_new_click(shortener)
            return redirect(shortener.url)
        else:
            raise Http404
