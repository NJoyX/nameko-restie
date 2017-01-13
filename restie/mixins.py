from nameko.web.handlers import HttpRequestHandler

from .constants import ALL_HTTP_METHODS


class HttpCORSMixin(HttpRequestHandler):
    # @TODO rewrite into nameko Entrypoint (restie module named DecoratorEntrypoint)
    def _methods(self, default=None):
        _methods = []
        map(lambda z: _methods.extend(getattr(self, z, [None])), ['method', 'methods', 'METHOD', 'METHODS'])
        _methods = filter(None, _methods)
        return list(_methods) if _methods else default

    def handle_request(self, request):
        response = super(HttpCORSMixin, self).handle_request(request=request)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Authentication,Authorization')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', ', '.join(
            list(set(self._methods(default=ALL_HTTP_METHODS)))
        ))
        response.headers.add('Access-Control-Expose-Headers', 'Location,X-Status,X-Count-Total,X-Pages-Total')
        response.headers.add('Access-Control-Max-Age', 86400)
        return response
