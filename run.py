#!flask/bin/python
from app import app

app.debug = True

if __name__ == '__main__':
    app.run(host="127.0.0.1", threaded=True)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
