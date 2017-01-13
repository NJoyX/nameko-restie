from __future__ import unicode_literals, print_function, absolute_import

from collections import OrderedDict

from nameko.exceptions import safe_for_serialization
from restie.utils import json
from restie.exceptions import HttpError
from restie.utils import response_triple
from werkzeug.wrappers import Response

from .base import MethodsDecoratorEntrypoint
from .collector import ApiMethodsCollector

__author__ = 'Fill Q'
__all__ = ['JSONify']


class JSONify(MethodsDecoratorEntrypoint):
    collector = ApiMethodsCollector()

    def setup(self):
        self.collector.register_provider(self)

    def stop(self):
        self.collector.unregister_provider(self)
        super(JSONify, self).stop()

    def process_response(self, response, request, *args, **kwargs):
        if isinstance(response, Response):
            return response

        indent = None
        separators = (',', ':')

        if not request.is_xhr:
            indent = 2
            separators = (', ', ': ')

        status, headers, payload = response_triple(response)

        if not isinstance(headers, dict):
            headers = {}

        if isinstance(payload, (dict, list, tuple, set, int)) or payload is None or payload is True or payload is False:
            try:
                payload = json.dumps(
                    payload,
                    indent=indent,
                    ensure_ascii=False,
                    separators=separators,
                    encoding='utf-8'
                )
                headers.update({'Content-Type': 'application/json; charset=utf-8'})
            except (TypeError, ValueError):
                pass
        return Response(
            payload,
            status=status,
            headers=headers
        )

    def process_exception(self, request, exc, *args, **kwargs):
        if isinstance(exc, HttpError):
            if isinstance(exc.message, (list, tuple, dict, OrderedDict)):
                _msg = exc.message
            else:
                _msg = safe_for_serialization(exc)
            response = Response(
                json.dumps({
                    'error': exc.error_code,
                    'message': _msg,
                }),
                status=exc.status_code,
                mimetype='application/json'
            )
            return response
        return
