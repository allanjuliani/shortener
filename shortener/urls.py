from django.contrib import admin
from django.urls import path

from shortener.views import error_404, get_shortend_and_redirect  # , home

handler404 = error_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '<str:shortened>',
        get_shortend_and_redirect,
        name='get-shortend-and-redirect',
    ),
    # path('', home, name='home'),
]
