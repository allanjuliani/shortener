from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
from shortener.models import Shortener, Log


def get_ip(request):
    # try:
    #     real_ip = request.META.get('HTTP_X_FORWARDED_FOR').split(', ')[0]
    # except AttributeError:
    #     real_ip = request.META.get('HTTP_X_REAL_IP')
    # if not real_ip:
    #     real_ip = request.META.get('REMOTE_ADDR')

    # if real_ip == '127.0.0.1' or real_ip == '10.0.0.58':
    #     real_ip = '201.6.116.151'

    # return real_ip
    return "179.174.41.29"


def get_ip_info(ip):
    context = {
        'latitude': None,
        'longitude': None,
        'city': None,
        'state': None,
        'country': None,
    }

    try:
        geo = GeoIP2()
        locale = geo.city(ip)

    except AddressNotFoundError:
        pass

    else:
        context = {
            'latitude': str(locale.get('latitude'))[:8],
            'longitude': str(locale.get('longitude'))[:8],
            'city': locale.get('city'),
            'state': locale.get('region'),
            'country': locale.get('country_name'),
        }

    return context


def get_browser_info(request):
    http_user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(http_user_agent)
    browser = '%s %s' % (user_agent.browser.family, user_agent.browser.version_string)
    os = '%s %s' % (user_agent.os.family, user_agent.os.version_string)

    context = {
        'browser': browser,
        'os': os,
        'user_agent': user_agent,
    }

    return context



def error_404(request, exception=None):
    if exception:
        pass

    return render(request, 'error/404.html')


def get_shortend_and_redirect(request, shortened):
    shortener = Shortener.objects.filter(shortened__exact=shortened).first()

    if shortener:
        ip = get_ip(request)
        ip_info = get_ip_info(ip)
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

        return redirect(shortener.url)

    else:
        raise Http404


# def home(request):
#     return redirect(settings.PORTAL_URL)
