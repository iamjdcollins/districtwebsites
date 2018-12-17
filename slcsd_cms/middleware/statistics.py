import threading
import uuid
from copy import deepcopy

from django.utils import timezone

from ..models import Request


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def seconds_to_milliseconds(seconds):
    return int(seconds * 1000)


def build_request_values(request, response):
    defaults = {
        'scheme': request.scheme,
        'host': request.get_host(),
        'path': request.get_full_path_info(),
        'method': request.method,
        'encoding': request.encoding,
        'request_content_type': request.content_type,
        'request_content_length': (
            request.META['CONTENT_LENGTH'] or 0 if 'CONTENT_LENGTH' in
                                                   request.META else 0
        ),
        'secure': request.is_secure(),
        'ajax': request.is_ajax(),
        'remote_address': request.remote_address,
        'status_code': response.status_code,
    }
    # Copy headers so that I can remove headers that are mapped.
    request_headers = {}
    for key, value in request.META.items():
        if key.startswith('HTTP_'):
            request_headers[key] = value
    mapped_request_headers = (
        'HTTP_ACCEPT',
        'HTTP_USER_AGENT',
        'HTTP_CACHE_CONTROL',
        'HTTP_ACCEPT_LANGUAGE',
        'HTTP_CONNECTION',
        'HTTP_ACCEPT_ENCODING',
        'HTTP_REFERER',
    )
    for header in mapped_request_headers:
        if header in request_headers:
            # Strip off HTTP_ and lower.
            defaults[header[5:].lower()] = request_headers[header]
            del request_headers[header]
    defaults['remaining_request_headers'] = request_headers
    response_headers = {}
    for key, value in response._headers.items():
        response_headers[key] = value
    mapped_response_headers = (
        'content-type',
        'content-length',
        'vary',
        'x-frame-options',
    )
    for header in mapped_response_headers:
        if header in response_headers:
            field = 'response_{0}'.format(header.lower().replace('-', '_'))
            defaults[field] = response.__getitem__(header)
            del response_headers[header]
    defaults['remaining_response_headers'] = response_headers
    defaults['site'] = request.site if hasattr(request, 'site') else None
    defaults['user'] = request.user if hasattr(request, 'user') else None
    if defaults['user']:
        defaults['user'] = defaults['user'] if defaults[
            'user'].is_authenticated else None
    defaults['session'] = (
        request.session.session_key if hasattr(request, 'session') else None
    )
    defaults['create_date'] = request.start_time
    defaults['update_date'] = timezone.localtime()
    defaults['processing_time'] = seconds_to_milliseconds(
        (defaults['update_date'] - defaults['create_date']).total_seconds()
    )
    return defaults


def log_request(defaults):
    r, created = Request.objects.get_or_create(
        uuid=uuid.uuid4(),
        defaults=defaults,
    )


class Statistics:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        request.remote_address = get_client_ip(request)
        request.start_time = timezone.localtime()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        defaults = build_request_values(request, response)
        t = threading.Thread(target=log_request, args=(defaults,))
        t.daemon = False
        t.name = 'StatisticsMiddleware'
        t.start()
        return response
