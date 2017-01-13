from __future__ import absolute_import

from apispec import APISpec as MApiSpec
from nameko.extensions import ENTRYPOINT_EXTENSIONS_ATTR
from werkzeug.wrappers import Request

__all__ = ['APISpec']


class APISpec(MApiSpec):
    def __init__(self, title=None, version=None, plugins=(), info=None, **options):
        title = title or 'Restie'
        version = version or '0.1'
        plugins += tuple(set(
            plugins + ('apispec.ext.marshmallow', 'restie.apispec.ext.werkzeug')
        ))
        super(APISpec, self).__init__(
            title=title, version=version, plugins=plugins, info=info, **options
        )

    def __call__(self, fn):
        for entrypoint in getattr(fn, ENTRYPOINT_EXTENSIONS_ATTR, set()):
            if not hasattr(entrypoint, 'get_url_rule'):
                continue
            self.add_path(view=fn, rule=entrypoint.get_url_rule())
        return fn

    def to_dict(self, request=None):
        ret = super(APISpec, self).to_dict()
        if isinstance(request, Request):
            ret.update({
                'host': request.host,
                'schemes': [request.scheme]
            })
        return ret
