from collections import namedtuple

from nameko.extensions import DependencyProvider


class ServiceDependencyProvider(DependencyProvider):
    def make_dependency(self, **services):
        return namedtuple('{}Dependency'.format(self.__class__.__name__), services.keys())(**services)

    def get_dependency(self, worker_ctx):
        return self.make_dependency(**getattr(self, 'services', {}))
