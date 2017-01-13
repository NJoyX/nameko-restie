from __future__ import unicode_literals, print_function, absolute_import

from restie.base import ServiceDependencyProvider
from restie.model import BaseRestModel

from .methods import MarshalWith, Expect, JSONify

__all__ = ['API']


class API(ServiceDependencyProvider):
    marshal_with = MarshalWith.decorator
    expect = Expect.decorator
    jsonify = JSONify.decorator

    def get_dependency(self, worker_ctx):
        return self.make_dependency(**dict(
            marshal_with=self.marshal_with,
            expect=self.expect,
            jsonify=self.jsonify
        ))

    @classmethod
    def model(cls, name, fields=None, **kw_fields):
        if isinstance(fields, dict):
            fields.update(kw_fields)
        return type(name, (BaseRestModel,), fields)
