import os
import sys

class Commenter(object):
    def __init__(self, app, storage_dir):
        self.app = app
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def __call__(self, environ, start_response):
        from webob import Request
        req = Request(environ)
        resp = req.get_response(self.app)
        return resp(environ, start_response)

    #STARTNEW
    def get_data(self, url):
        from cPickle import load
        filename = self.url_filename(url)
        if not os.path.exists(filename):
            return []
        else:
            f = open(filename, 'rb')
            data = load(f)
            f.close()
            return data

    def save_data(self, url, data):
        from cPickle import dump
        filename = self.url_filename(url)
        f = open(filename, 'wb')
        dump(data, f)
        f.close()

    def url_filename(self, url):
        # Double-quoting makes the filename safe
        import urllib
        return os.path.join(self.storage_dir, urllib.quote(url, ''))
    #ENDNEW

if __name__ == '__main__':
    from paste.urlparser import StaticURLParser
    from paste import httpserver
    app = StaticURLParser(sys.argv[1])
    app = Commenter(app, sys.argv[2])
    httpserver.serve(
        app, host='127.0.0.1', port=8080)
