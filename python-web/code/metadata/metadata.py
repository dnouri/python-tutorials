import datetime
import os
import webob

class MetadataApp(object):
    def __init__(self, document_root):
        self.document_root = document_root

    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        resp = webob.Response(
            self.format_metadata(req))
        return resp(environ, start_response)

    def format_metadata(self, req):
        path = os.path.join(
            self.document_root,
            req.path_info.lstrip('/'))
        if not os.path.exists(path):
            return 'No such file <em>%s</em>' % path
        else:
            stat = os.stat(path)
            make_date = datetime.datetime.fromtimestamp
            return """
            Size: %s Bytes<br/>
            Created: %s<br/>
            Modified: %s<br/>
            Last access: %s<br/>
            """ % (
            stat.st_size,
            make_date(stat.st_ctime),
            make_date(stat.st_mtime),
            make_date(stat.st_atime),
            )

def app_factory(global_config, document_root):
    return MetadataApp(document_root)
