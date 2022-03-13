from django.contrib import admin
from django.urls import path

from apps.shortener.views import RedirectToShortenedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '<str:code>',
        RedirectToShortenedView.as_view(),
        name='redirect-to-shortened',
    ),
]
