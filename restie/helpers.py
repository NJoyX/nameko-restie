from __future__ import absolute_import, print_function, unicode_literals

import sys
import types
from functools import partial
from functools import wraps

import six
from nameko.extensions import ProviderCollector, SharedExtension, ENTRYPOINT_EXTENSIONS_ATTR, Entrypoint, \
    register_entrypoint
from werkzeug.wrappers import Request, Response


class DecoratorCollector(ProviderCollector, SharedExtension):
    def start(self):
        for provider in filter(lambda p: isinstance(p, DecoratorEntrypoint), self._providers):
            provider.method = self.decorate_method(provider, provider.method)

    def decorate_method(self, provider, fn):
        method_attrs = getattr(fn, ENTRYPOINT_EXTENSIONS_ATTR, set())

        @wraps(fn)
        def wrapper(this, request, *args, **kwargs):
            try:
                request = self.before_method_call(provider, request, *args, **kwargs)
                response = fn(this, request, *args, **kwargs)
                return self.after_method_call(provider, response, request, *args, **kwargs)
            except Exception as exc:
                return self.on_exception(provider, request, exc, *args, **kwargs)

        setattr(wrapper, ENTRYPOINT_EXTENSIONS_ATTR, method_attrs)
        return wrapper

    @staticmethod
    def before_method_call(provider, request, *args, **kwargs):
        result = None
        _callable = getattr(provider, 'process_request', None)

        if callable(_callable):
            result = _callable(request, *args, **kwargs)

        if isinstance(result, Request):
            return result
        return request

    @staticmethod
    def after_method_call(provider, response, request, *args, **kwargs):
        result = None
        _callable = getattr(provider, 'process_response', None)

        if callable(_callable):
            result = _callable(response, request, *args, **kwargs)

        if result is not None or isinstance(result, Response):
            return result
        return response

    @staticmethod
    def on_exception(provider, request, exc, *args, **kwargs):
        result = None
        _callable = getattr(provider, 'process_exception', None)

        if callable(_callable):
            result = _callable(request, exc, *args, **kwargs)

        if result is not None or isinstance(result, Response):
            return result

        six.reraise(*sys.exc_info())


class DecoratorEntrypoint(Entrypoint):
    def setup(self):
        raise NotImplementedError('Implement setup in class "%s"' % '.'.join([
            self.__class__.__module__,
            self.__class__.__name__
        ]))

    def stop(self):
        super(DecoratorEntrypoint, self).stop()

    @property
    def service_cls(self):
        return self.container.service_cls

    @property
    def method(self):
        return getattr(self.service_cls, self.method_name)

    @method.setter
    def method(self, meth):
        setattr(self.container.service_cls, self.method_name, meth)

    def process_request(self, request, *args, **kwargs):
        return request

    def process_response(self, response, request, *args, **kwargs):
        return response

    def process_exception(self, request, exc, *args, **kwargs):
        pass

    @classmethod
    def decorator(cls, *args, **kwargs):
        def registering_decorator(fn, a, kw):
            instance = cls(*a, **kw)
            register_entrypoint(fn, instance)
            return fn

        if len(args) >= 1 and isinstance(args[0], types.FunctionType):
            return registering_decorator(args[0], a=args[1:], kw=kwargs)

        return partial(registering_decorator, a=args, kw=kwargs)
