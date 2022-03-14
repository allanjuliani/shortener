from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DarkThemeConfig(AppConfig):
    name = 'apps.darktheme'
    verbose_name = _('DarkTheme')
