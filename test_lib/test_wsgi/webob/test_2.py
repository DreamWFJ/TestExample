from webob import Request, Response
import os

class FileApp(object):
    def __init__(self, filename):
        self.filename = filename
    def __call__(self, environ, start_response):
        res = make_response(self.filename)
        return res(environ, start_response)

import mimetypes

def get_mimetype(filename):
    type, encoding = mimetypes.guess_type(filename)
    print "======",type, encoding
    return  type or 'application/octed-stream'

def make_response(filename):
    res = Response(content_type=get_mimetype(filename))
    res.body = open(filename, 'rb').read()
    return res

if __name__ == '__main__':
    app = FileApp('test-file.txt')
    req = Request.blank('/')
    print req.get_response(app)