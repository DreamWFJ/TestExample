import os
import webob
from webob import Response,Request
from paste.deploy import loadapp
from wsgiref.simple_server import make_server

class ShowVersion(object):
      '''
      app
      '''
      def __init__(self,version):
          self.version = version
      def __call__(self,environ,start_response):
          res = Response()
          res.status = '200 OK'
          res.content_type = "text/plain"
          content = []
          content.append("%s\n" % self.version)
          res.body = '\n'.join(content)
          return res(environ,start_response)
      @classmethod
      def factory(cls,global_conf,**kwargs):
          print 'factory'
          print "kwargs:",kwargs
          return ShowVersion(kwargs['version'])

class LogFilter(object):
      '''
      Log
      '''
      def __init__(self,app):
          self.app = app
      def __call__(self,environ,start_response):
          print 'you can write log.'
          return self.app(environ,start_response)
      @classmethod
      def factory(cls,global_conf,**kwargs):
          return LogFilter



config = "test_2.ini"
appname = "common"
wsgi_app = loadapp("config:%s" % os.path.abspath(config), appname)
server = make_server('localhost',80,wsgi_app)
server.serve_forever()