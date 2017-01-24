from webob import Response, Request

def my_app(environ, start_response):
    req = Request(environ)
    res = Response()
    res.content_type = 'text/plain'
    parts = []
    for name, value in sorted(req.environ.items()):
        parts.append('%s: %r'%(name, value))
    res.body = '\n'.join(parts)
    return res(environ, start_response)

req = Request.blank('/')
res = req.get_response(my_app)
print res