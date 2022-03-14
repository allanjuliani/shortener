import random
import string
from typing import Dict, Optional

from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geoip2.base import GeoIP2Exception
from django.http import HttpRequest
from geoip2.errors import AddressNotFoundError  # type: ignore
from user_agents import parse

from apps.shortener.models import Shortener


def add_new_click(shortener: Shortener) -> None:
    Shortener.objects.update(clicks=shortener.clicks + 1)


def random_generator() -> str:
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(5))


def generate_shortened_code() -> str:
    code = random_generator()

    while Shortener.objects.filter(shortened__exact=code).exists():
        code = random_generator()

    return code


def get_ip(request: HttpRequest) -> str:
    try:
        real_ip = request.META.get('HTTP_X_FORWARDED_FOR').split(', ')[0]
    except AttributeError:
        real_ip = request.META.get('HTTP_X_REAL_IP')
    if not real_ip:
        real_ip = request.META.get('REMOTE_ADDR')

    if real_ip == '127.0.0.1':
        real_ip = '201.6.116.151'

    return real_ip


def get_ip_info(request: HttpRequest) -> Dict[str, Optional[str]]:
    context = dict()
    ip = get_ip(request)

    try:
        locale = GeoIP2().city(ip)
        context.update(
            {
                'latitude': str(locale.get('latitude'))[:8],
                'longitude': str(locale.get('longitude'))[:8],
                'city': locale.get('city'),
                'state': locale.get('region'),
                'country': locale.get('country_name'),
            }
        )

    except (AddressNotFoundError, GeoIP2Exception):
        context.update(
            {
                'latitude': None,
                'longitude': None,
                'city': None,
                'state': None,
                'country': None,
            }
        )
    return context


def get_browser_info(request: HttpRequest) -> dict:
    http_user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(http_user_agent)
    browser = '%s %s' % (
        user_agent.browser.family,
        user_agent.browser.version_string,
    )
    os = '%s %s' % (user_agent.os.family, user_agent.os.version_string)

    context = {
        'browser': browser,
        'os': os,
        'user_agent': user_agent,
    }

    return context


def create_access_log(request: HttpRequest, shortener: Shortener) -> None:
    from apps.shortener.models import Log

    ip_info = get_ip_info(request)
    browser_info = get_browser_info(request)
    Log.objects.create(
        shortener_id=shortener.id,
        ip=get_ip(request),
        latitude=ip_info.get('latitude'),
        longitude=ip_info.get('longitude'),
        city=ip_info.get('city'),
        state=ip_info.get('state'),
        country=ip_info.get('country'),
        user_agent=browser_info.get('user_agent'),
        browser=browser_info.get('browser'),
        os=browser_info.get('os'),
    )


def get_shortener(code: str) -> Shortener:
    from apps.shortener.models import Shortener

    return Shortener.objects.filter(shortened__exact=code).first()
