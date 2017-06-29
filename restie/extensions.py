import os
import sys

import six
from nameko.web.handlers import HttpRequestHandler
from werkzeug.routing import Rule

from .constants import ALL_HTTP_METHODS
from .exceptions import HttpError
from .mixins import HttpCORSMixin
from .webserver import WebServer
from .utils import prefix_urls


class HttpRequestExtension(HttpRequestHandler):
    METHODS = ALL_HTTP_METHODS

    def __init__(self, methods, url, **kwargs):
        methods = self.METHODS = filter(lambda m: m in self.METHODS, list(self._get_methods(methods))) + ['OPTIONS']
        kwargs.setdefault('expected_exceptions', tuple())
        kwargs['expected_exceptions'] += (HttpError,)
        super(HttpRequestExtension, self).__init__(method=methods, url=url, **kwargs)

    @staticmethod
    def _get_methods(methods):
        if isinstance(methods, (six.text_type,) + six.string_types):
            methods = [methods]
        return filter(None, methods)

    def get_url_rule(self):
        if self.url is None:
            self.url = prefix_urls(self.container.service_name)
        _filtered_methods = filter(lambda x: x in self.METHODS, list(self.method))
        return Rule(self.url, methods=_filtered_methods or self.METHODS[:1])


class HttpEntrypoint(HttpRequestExtension, HttpCORSMixin):
    server = WebServer()

    @property
    def is_debug(self):
        return bool(self.container.config.get('DEBUG', os.environ.get('DEBUG', False))) is True

    def handle_request(self, request):
        return HttpCORSMixin.handle_request(self, request)

    def response_from_exception(self, exc):
        if self.is_debug:
            six.reraise(*sys.exc_info())
        response = super(HttpEntrypoint, self).response_from_exception(exc)
        if hasattr(exc, 'status_code'):
            response.status_code = exc.status_code
        return response


http = HttpEntrypoint.decorator
