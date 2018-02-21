import gevent.monkey
gevent.monkey.patch_all()

import logging
handler = logging.StreamHandler()
log_format = '{levelname}:onthehouse.{module}.{funcName}: {message}'
handler.setFormatter(logging.Formatter(log_format, style='{'))
logging.getLogger().addHandler(handler)

import onthehouse_flask
import gevent.pywsgi
import sys

import werkzeug.contrib.fixers
onthehouse_flask.site.wsgi_app = werkzeug.contrib.fixers.ProxyFix(onthehouse_flask.site.wsgi_app)


if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    port = 5000

http = gevent.pywsgi.WSGIServer(
    listener=('0.0.0.0', port),
    application=onthehouse_flask.site,
)


print('Starting server on port %d' % port)
http.serve_forever()


