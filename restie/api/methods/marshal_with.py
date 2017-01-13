from __future__ import unicode_literals, print_function, absolute_import

from marshmallow import MarshalResult
from marshmallow import Schema, ValidationError
from restie.exceptions import InvalidArgumentsError
from werkzeug.datastructures import CombinedMultiDict, MultiDict

from .base import MethodsDecoratorEntrypoint
from .collector import ApiMethodsCollector


class MarshalWith(MethodsDecoratorEntrypoint):
    collector = ApiMethodsCollector()

    def __init__(self, schema, strict=True, **kwargs):
        assert issubclass(schema, Schema), 'Invalid schema!'
        self.schema = schema(strict=strict, **kwargs)

    def setup(self):
        self.collector.register_provider(self)

    def stop(self):
        self.collector.unregister_provider(self)
        super(MarshalWith, self).stop()

    def validate(self, request, **kwargs):
        payload = CombinedMultiDict([
            request.args.copy(),
            request.form.copy(),
            MultiDict(kwargs.copy())
        ])
        return self.schema.dump(payload).data, self.schema.validate(payload)

    def process_request(self, request, *args, **kwargs):
        try:
            data, errors = self.validate(request, **kwargs)
            if errors:
                raise InvalidArgumentsError(errors)
        except ValidationError as e:
            raise InvalidArgumentsError(e.messages)

        setattr(request, 'valid', MarshalResult(data, errors))
        return request
