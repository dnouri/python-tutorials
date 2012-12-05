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
        if req.path_info_peek() == '.comments':
            return self.process_comment(req)(environ, start_response)

        # URL without PATH_INFO:
        base_url = req.application_url
        resp = req.get_response(self.app)
        if resp.content_type != 'text/html' or resp.status_int != 200:
            # Not an HTML response, we don't want to
            # do anything to it
            return resp(environ, start_response)
        # Make sure the content isn't gzipped:
        resp.decode_content()
        comments = self.get_data(req.url)
        body = resp.body
        body = self.add_to_end(body, self.format_comments(comments))
        body = self.add_to_end(body, self.submit_form(base_url, req))
        resp.body = body
        return resp(environ, start_response)
    #ENDNEW

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

    import re
    _end_body_re = re.compile(r'</body.*?>', re.I|re.S)

    def add_to_end(self, html, extra_html):
        match = self._end_body_re.search(html)
        if not match:
            return html + extra_html
        else:
            return html[:match.start()] + extra_html + html[match.start():]

    def format_comments(self, comments):
        import time
        from webob import html_escape
        if not comments:
            return ''
        text = []
        text.append('<hr>')
        text.append('<h2><a name="comment-area"></a>Comments (%s):</h2>' % len(comments))
        for comment in comments:
            text.append('<h3><a href="%s">%s</a> at %s:</h3>' % (
                html_escape(comment['homepage']), html_escape(comment['name']),
                time.strftime('%c', comment['time'])))
            # Susceptible to XSS attacks!:
            text.append(comment['comments'])
        return ''.join(text)

if __name__ == '__main__':
    from paste.urlparser import StaticURLParser
    from paste import httpserver
    app = StaticURLParser(sys.argv[1])
    app = Commenter(app, sys.argv[2])
    httpserver.serve(
        app, host='127.0.0.1', port=8080)
