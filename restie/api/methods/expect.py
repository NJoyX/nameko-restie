from __future__ import unicode_literals, print_function, absolute_import

from apispec import APISpec
from marshmallow import Schema
from restie.utils import response_triple
from werkzeug.wrappers import Response

from .base import MethodsDecoratorEntrypoint
from .collector import ApiMethodsCollector

__all__ = ['Expect']


class Expect(MethodsDecoratorEntrypoint):
    collector = ApiMethodsCollector()

    def __init__(self, schema, spec=None, many=False, **kwargs):
        assert issubclass(schema, Schema), 'Invalid schema!'
        self.schema_cls = schema
        self.schema = schema(strict=False, many=many, **kwargs)
        self.many = many
        self.register_definition(spec)

    def setup(self):
        self.collector.register_provider(self)

    def stop(self):
        self.collector.unregister_provider(self)
        super(Expect, self).stop()

    def process_response(self, response, request, *args, **kwargs):
        if isinstance(response, Response):
            return response

        status, headers, payload = response_triple(response)
        return status, headers, self.validate(payload)

    def validate(self, payload=None):
        return self.schema.dump(payload).data

    def register_definition(self, spec=None):
        if not isinstance(spec, APISpec):
            return

        schema_cls = self.schema_cls
        name = getattr(getattr(schema_cls, 'Meta', object), 'title', type(self.schema).__name__)
        spec.definition(name, schema=self.schema_cls)
