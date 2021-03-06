import inspect

from nameko.exceptions import IncorrectSignature
from werkzeug.utils import import_string


class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value


CONSTANTS = _const()


def check_signature(fn, args, kwargs):
    try:
        inspect.getcallargs(fn, *args, **kwargs)
    except TypeError as exc:
        raise IncorrectSignature(str(exc))


def response_triple(result):
    headers = None
    if isinstance(result, tuple):
        if len(result) == 3:
            status, headers, payload = result
        else:
            status, payload = result
    else:
        payload = result
        status = 200

    return status, headers, payload


prefix_urls = lambda z: ('/api/%s/' % z).replace('//', '/')

json = filter(None, map(lambda j: import_string(j, silent=True), [
    'rapidjson',
    'ujson',
    'simplejson',
    'json'
]))[0]
