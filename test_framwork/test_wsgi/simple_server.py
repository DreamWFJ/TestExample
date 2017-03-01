# -*- coding: utf-8 -*-
# ===================================
# ScriptName : simple_server.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-02-15 15:47
# ===================================
# Our tutorial's WSGI server
from wsgiref.simple_server import make_server

def application(environ, start_response):

   # Sorting and stringifying the environment key, value pairs
   response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
   response_body = '\n'.join(response_body)

   status = '200 OK'
   response_headers = [('Content-Type', 'text/plain'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)

   return [response_body]

# Instantiate the WSGI server.
# It will receive the request, pass it to the application
# and send the application's response to the client
httpd = make_server(
   'localhost', # The host name.
   8051, # A port number where to wait for the request.
   application # Our application object name, in this case a function.
   )

httpd.serve_forever()
