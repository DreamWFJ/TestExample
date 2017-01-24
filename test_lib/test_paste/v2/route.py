from webob.dec import wsgify
import webob.exc
import json
from routes import Mapper, middleware

class Controller(object):
    def help(self):
        return "help()"
    def info(self):
        return "info()"

class InfoManage(object):
    def __init__(self):
        self.controller = Controller()
        self.mapper = Mapper()
        self.mapper.connect('info', '/', method='info')
        self.mapper.connect('info', '/info/help', method='help')
        self.router = middleware.RoutesMiddleware(self._dispatch, self.mapper)

    @wsgify
    def __call__(self, req):
        return self.router

    @wsgify
    def _dispatch(self, req):
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        action = match['action']
        if hasattr(self.controller, action):
            ret = getattr(self.controller, action)
            return ret
        else:
            return webob.exc.HTTPMethodNotAllowed()



    @staticmethod
    def factory(cls):
        return InfoManage()