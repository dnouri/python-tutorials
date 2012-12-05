import sys
from paste.urlparser import StaticURLParser
from paste import httpserver

if __name__ == '__main__':
    app = StaticURLParser(sys.argv[1])
    httpserver.serve(
        app, host='127.0.0.1', port=8080)
