# -*- coding:utf-8 -*-
from wsgiref.simple_server import make_server
CONTENT_TYPE = 'text/plain;charset=utf-8'

def application(environ, start_response):
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)
    response_body = [
        'The Beggining\n',
        '*' * 30 + '\n',
        response_body,
        '\n' + '*' * 30 ,
        '\nThe End'
    ]

    content_length = sum([len(s) for s in response_body])

    status = '200 OK'
    response_headers = [
        ('Content-Type', CONTENT_TYPE),
        ('Content-Length', str(content_length))
    ]

    start_response(status, response_headers)

    unicodeText = u'<h1>Hello, 小明</h1><br>%s'%response_body
    return unicodeText.encode('utf-8')

class App(object):
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-Type', 'text/html')]
        self.start_response(status, response_headers)
        yield 'hello world'

httpd = make_server('', 8000, application)
print 'Serving HTTP on port 8000...'
httpd.serve_forever()