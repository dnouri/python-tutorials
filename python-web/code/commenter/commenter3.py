import os
import sys

class Commenter(object):
    def __init__(self, app, storage_dir):
        self.app = app
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    #STARTNEW
    def __call__(self, environ, start_response):
        from webob import Request
        req = Request(environ)
        resp = req.get_response(self.app)
        return resp(environ, start_response)
    #ENDNEW

if __name__ == '__main__':
    from paste.urlparser import StaticURLParser
    from paste import httpserver
    app = StaticURLParser(sys.argv[1])
    app = Commenter(app, sys.argv[2])
    httpserver.serve(
        app, host='127.0.0.1', port=8080)
