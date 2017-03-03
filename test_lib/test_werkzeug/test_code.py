# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_code.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-01 15:07
# ===================================

from werkzeug.routing import Map, Rule, Subdomain

def test_1():
    m = Map([
        Rule('/', endpoint='index'),
        Rule('/downloads/', endpoint='downloads/index'),
        Rule('/downloads/<int:id>', endpoint='downloads/show')
    ])
    urls = m.bind("example.com", "/")
    print urls.match("/", "GET")
    print urls.match("/downloads/42")
    print urls.build("index", {})
    print urls.build("downloads/show", {'id': 42})
    print urls.build("downloads/show", {'id': 42}, force_external=True)

def test_2():
    m = Map([
        Rule('/', endpoint='static/index'),
        Rule('/about', endpoint='static/about'),
        Rule('/help', endpoint='static/help'),
        Subdomain('kb', [
            Rule('/', endpoint='kb/index'),
            Rule('/browse/', endpoint='kb/browse'),
            Rule('/browse/<int:id>/', endpoint='kb/browse'),
            Rule('/browse/<int:id>/<int:page>', endpoint='kb/browse')
        ])
    ], default_subdomain='www')
    c = m.bind('example.com')
    print c.build("kb/browse", dict(id=42))
    print c.build("kb/browse", dict())
    print c.build("kb/browse", dict(id=42, page=3))
    print c.build("static/about")
    print c.build("static/index", force_external=True)
    c = m.bind('example.com', subdomain='kb')
    print c.build("static/about")
    c = m.bind('example.com', '/applications/example')

    c = m.bind('example.com')
    print c.match("/")
    print c.match("/about")
    c = m.bind('example.com', '/', 'kb')
    print c.match("/")
    print c.match("/browse/42/23")

if __name__ == '__main__':
    # test_1()
    test_2()
    