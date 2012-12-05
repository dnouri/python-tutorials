import os
import sys

class Commenter(object):
    def __init__(self, app, storage_dir):
        self.app = app
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

#STARTNEW
if __name__ == '__main__':
    from paste.urlparser import StaticURLParser
    from paste import httpserver
    app = StaticURLParser(sys.argv[1])
    app = Commenter(app, sys.argv[2])
    httpserver.serve(
        app, host='127.0.0.1', port=8080)
