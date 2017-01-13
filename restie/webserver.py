import os
import sys

import eventlet
from eventlet.green import socket
from nameko.constants import WEB_SERVER_CONFIG_KEY
from nameko.web.server import WebServer as NamekoWebServer, parse_address
from werkzeug.debug import DebuggedApplication

__all__ = ['WebServer']


class WebServer(NamekoWebServer):

    @property
    def bind_addr(self):
        _default = '0.0.0.0:8000'
        address_str = self.container.config.get(
            WEB_SERVER_CONFIG_KEY, _default)
        if address_str.startswith('fd://'):
            address_str = _default
        return parse_address(address_str)

    @property
    def _sock_listen(self):
        address_str = self.container.config.get(WEB_SERVER_CONFIG_KEY, '')
        family = socket.AF_INET
        if address_str.startswith('fd://'):
            fd = int(address_str.split('://')[1])
            try:
                sock = socket.fromfd(fd, family, socket.SOCK_STREAM)
                if sys.platform[:3] != "win":
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if hasattr(socket, 'SO_REUSEPORT'):
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                return sock
            except socket.error:
                pass

        return eventlet.listen(self.bind_addr, family, backlog=2048)

    def start(self):
        if not self._starting:
            self._starting = True
            self._sock = self._sock_listen
            self._serv = self.get_wsgi_server(self._sock, self.get_wsgi_app())
            self._gt = self.container.spawn_managed_thread(self.run)

    def get_wsgi_app(self):
        wsgi_app = super(WebServer, self).get_wsgi_app()
        if 'DEBUG' in os.environ:
            return DebuggedApplication(wsgi_app, evalex=True)
        return wsgi_app
