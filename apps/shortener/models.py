from django.db import models
from django.utils.translation import gettext_lazy as _


class Shortener(models.Model):
    url = models.URLField(_('URL'), unique=True)
    shortened = models.CharField(
        _('Shortened'), max_length=5, unique=True, blank=True
    )
    clicks = models.IntegerField(_('Clicks'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        db_table = 'shortener'
        verbose_name = _('Shortener')
        verbose_name_plural = _('Shorteners')

    def __str__(self):
        return self.shortened

    def save(self, *args, **kwargs):
        from apps.shortener.utils import generate_shortened_code

        if not self.shortened:
            self.shortened = generate_shortened_code()
        super().save(*args, **kwargs)


class Log(models.Model):
    shortener = models.ForeignKey(
        Shortener, verbose_name=_('Shortener'), on_delete=models.CASCADE
    )
    ip = models.GenericIPAddressField(_('IP'))
    user_agent = models.CharField(
        _('User Agent'), max_length=512, null=True, blank=True
    )
    browser = models.CharField(
        _('Browser'), max_length=50, null=True, blank=True
    )
    os = models.CharField(_('OS'), max_length=50, null=True, blank=True)
    latitude = models.CharField(
        _('Latitude'), max_length=8, null=True, blank=True
    )
    longitude = models.CharField(
        _('Longitude'), max_length=8, null=True, blank=True
    )
    city = models.CharField(_('City'), max_length=100, null=True, blank=True)
    state = models.CharField(_('State'), max_length=50, null=True, blank=True)
    country = models.CharField(
        _('Country'), max_length=50, null=True, blank=True
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        db_table = 'shortener_log'
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')
