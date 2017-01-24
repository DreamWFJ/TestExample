'''''
Created on 2013-10-28

@author: root
'''


import os
from paste.deploy import loadapp
from wsgiref.simple_server import make_server



if __name__ == '__main__':
    configfile="test-deploy.ini"
    appname="test_deploy"
    wsgi_app = loadapp("config:%s" % os.path.abspath(configfile), appname)
    server = make_server('localhost',8088,wsgi_app)
    server.serve_forever()
