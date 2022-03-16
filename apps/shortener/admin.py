from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Click, Shortener

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
    list_per_page = 10
    readonly_fields = ('session_key', 'expire_date', 'session_data')


@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        return ([] if obj else 'clicks_link',)

    def get_readonly_fields(self, request, obj=None):
        return (
            [
                'id',
                'url',
                'shortened_link',
                'clicks_link',
                'created_at',
                'updated_at',
            ]
            if obj
            else []
        )

    def get_fields(self, request, obj=None):
        return (
            [
                'id',
                'url',
                'shortened_link',
                'clicks_link',
                'created_at',
                'updated_at',
            ]
            if obj
            else ['url', 'shortened']
        )

    def shortened_link(self, obj):
        link = '{}{}'.format(settings.DOMAIN, obj.shortened)
        return format_html(
            '{link}&nbsp;<a target="_blank" class="viewlink" '
            'href="{link}"></a>',
            link=link,
        )

    shortened_link.short_description = _('Shortened')  # type: ignore
    shortened_link.admin_order_field = 'shortened'  # type: ignore

    def clicks_link(self, obj):
        return format_html(
            '<a href="{url}?shortener__id__exact={id}">{clicks}</a>',
            url=reverse('admin:shortener_click_changelist'),
            id=obj.id,
            clicks=obj.clicks,
        )

    clicks_link.short_description = _('Clicks')  # type: ignore
    clicks_link.admin_order_field = 'clicks'  # type: ignore

    list_display = (
        'id',
        'url',
        'shortened_link',
        'clicks_link',
        'created_at',
        'updated_at',
    )
    list_display_links = None
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20
    actions = None


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    def google_maps(self, obj):
        return format_html(
            '<iframe class="map" width="240" height="180" '
            'frameborder="0" scrolling="no" marginheight="0" '
            'marginwidth="0" '
            'src="https://maps.google.com/?ll={latitude},{longitude}'
            '&z=11&output=embed">'
            '</iframe>',
            latitude=obj.latitude,
            longitude=obj.longitude,
        )

    google_maps.short_description = _('Map')  # type: ignore

    def view_shortener(self, obj):
        return format_html(
            '<a href="{url}">{id}</a>',
            id=obj.shortener.shortened,
            url=reverse(
                'admin:shortener_shortener_change',
                args=(1,),
            ),
        )

    view_shortener.short_description = _('Shortener')  # type: ignore
    view_shortener.admin_order_field = '_shortener'  # type: ignore

    actions = None
    list_display = (
        'google_maps',
        'id',
        'view_shortener',
        'ip',
        'latitude',
        'longitude',
        'city',
        'state',
        'country',
        'user_agent',
        'browser',
        'os',
        'created_at',
    )
    list_display_links = None
    list_per_page = 10
    readonly_fields = list_display
    show_full_result_count = None
