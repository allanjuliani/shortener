from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from django.utils.html import format_html
from django.utils.translation import ugettext as _

from apps.shortener.models import Log, Shortener

admin.site.site_title = _('Shortener - Admin')
admin.site.site_header = admin.site.site_title
admin.site.index_title = _('Home')


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    actions = None
    list_display = (
        'id',
        'user',
        'action_time',
        'content_type',
        'object_id',
        'object_repr',
        'change_message',
        'action_flag',
    )
    list_filter = ('user', 'action_flag')
    list_per_page = 10
    readonly_fields = (
        'id',
        'user',
        'action_time',
        'content_type',
        'object_id',
        'object_repr',
        'change_message',
        'action_flag',
    )
    search_fields = ('object_repr', 'change_message')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('session_key', 'expire_date', 'session_data')
    list_display_links = None
    list_per_page = 500
    readonly_fields = ('session_key', 'expire_date', 'session_data')


@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        return ([] if obj else 'clicks',)

    def get_readonly_fields(self, request, obj=None):
        return ['id', 'url', '_shortened', 'clicks', 'date'] if obj else []

    def get_fields(self, request, obj=None):
        return (
            ['id', 'url', '_shortened', 'clicks', 'date']
            if obj
            else ['url', 'shortened']
        )

    def _shortened(self, obj):
        link = '{}{}'.format(settings.DOMAIN, obj.shortened)
        return format_html(
            '{link}&nbsp;<a target="_blank" class="viewlink"'
            'href="{link}"></a>',
            link=link,
        )

    _shortened.short_description = _('Shortened')  # type: ignore
    _shortened.admin_order_field = 'shortened'  # type: ignore

    def _clicks(self, obj):
        return format_html(
            '<a href="/admin/shortener/log/?shortener_id={}">{}</a>',
            obj.id,
            obj.clicks,
        )

    _clicks.short_description = _('Clicks')  # type: ignore
    _clicks.admin_order_field = 'clicks'  # type: ignore

    list_display = 'id', 'url', '_shortened', '_clicks', 'date'
    list_display_links = None
    list_per_page = 20
    actions = None


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    def map(self, obj):
        html = """
            <iframe class="map" width="240" height="180"
            frameborder="0" scrolling="no" marginheight="0"
            marginwidth="0"
            src="https://maps.google.com/?ll={},{}&z=11&output=embed">
            </iframe>
        """
        return format_html(html, obj.latitude, obj.longitude)

    map.short_description = _('Map')  # type: ignore

    def _shortener(self, obj):
        # link = '{}{}'.format(settings.DOMAIN, obj.shortener.shortened)
        link = '{}'.format(obj.shortener.shortened)
        return format_html(
            '<a href="/admin/shortener/shortener/{}/">{}</a>',
            obj.shortener_id,
            link,
        )

    _shortener.short_description = _('Shortener')  # type: ignore
    _shortener.admin_order_field = '_shortener'  # type: ignore

    actions = None
    list_display = (
        'map',
        'id',
        '_shortener',
        'ip',
        'latitude',
        'longitude',
        'city',
        'state',
        'country',
        'user_agent',
        'browser',
        'os',
        'date',
    )
    list_display_links = None
    list_per_page = 10
    # paginator = CachingPaginator
    # readonly_fields = list_display
    show_full_result_count = None
