from __future__ import unicode_literals, print_function, absolute_import

from restie.helpers import DecoratorEntrypoint

__all__ = ['MethodsDecoratorEntrypoint']


class MethodsDecoratorEntrypoint(DecoratorEntrypoint):
    @classmethod
    def first(cls, data, default=None):
        if not data:
            return default
        if not isinstance(data, (list, tuple)):
            data = [data]
        return iter(data).next() or default
