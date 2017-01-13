from nameko.web.websocket import *
from werkzeug.routing import Rule
from .webserver import WebServer

__all__ = ['Server', 'websocket', 'WebSocketHub', 'HubProvider']

_var = '_url_rule'
_default = '/ws'


class Server(WebSocketServer):
    wsgi_server = WebServer()

    @property
    def url_rule(self):
        return getattr(self, _var, Rule(_default, methods=['GET']))

    @url_rule.setter
    def url_rule(self, url):
        if not hasattr(self, _var):
            setattr(self, _var, Rule(url, methods=['GET']))

    def get_url_rule(self):
        return self.url_rule


class HubProvider(WebSocketHubProvider):
    server = Server()


class RPC(WebSocketRpc):
    server = Server()

    def __init__(self, url=_default):
        self.server.url_rule = url
        super(RPC, self).__init__()

websocket = RPC.decorator
