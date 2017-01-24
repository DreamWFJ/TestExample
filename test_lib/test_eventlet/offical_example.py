# -*- coding: utf-8 -*-
# ===================================
# ScriptName : offical_example.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-05 9:34
# ===================================
from __future__ import print_function
from __future__ import with_statement
import re
import eventlet
from eventlet import wsgi
from eventlet.green import urllib2
from eventlet.green import socket
from eventlet import websocket
from eventlet.support import six
from eventlet.green.OpenSSL import SSL

# demo app
import os
import random


def test_web_crawler():
    urls = [
        'http://docs.openstack.org/common/images/openstack-logo-full.png',
        'http://docs.openstack.org/common/images/docs/superuser4.png',
        'http://docs.openstack.org/common/images/footer-twitter.png',
    ]

    def fetch(url):
        print('opening ', url)
        body = urllib2.urlopen(url).read()
        print('done with ', url)
        return url, body

    pool = eventlet.GreenPool(200)
    for url, body in pool.imap(fetch, urls):
        print('got body from ', url, ' of lenth ', len(body))

def test_feed_scraper():
    feedparser = eventlet.import_patched('feedparser')
    pool = eventlet.GreenPool()

    def fetch_title(url):
        d = feedparser.parse(url)
        return d.feed.get('title', '')

    def app(environ, start_response):
        if environ['REQUEST_METHOD'] != 'POST':
            start_response('403 Forbidden', [])
            return []

        pile = eventlet.GreenPool(pool)
        for line in environ['wsgi.input'].readlines():
            url = line.strip()
            if url:
                pile.spawn(fetch_title, url)
        titles = '\n'.join(pile)
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [titles]

    wsgi.server(eventlet.listen(('', 8090)), app)


def test_wsgi_server():

    def hello_world(env, start_response):
        if env['PATH_INFO'] != '/':
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return ['Not Found\r\n']
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Hello, World!\r\n']


    wsgi.server(eventlet.listen(('', 8090)), hello_world)



def test_echo_server():
    def handle(fd):
        print('client connected')
        while True:
            x = fd.readline()
            if not x:
                break
            fd.write(x)
            fd.flush()
            print('echoed', x, end=' ')
        print('client disconnected')
    print('server socket listening on port 8090')
    server = eventlet.listen(('0.0.0.0', 8090))
    pool = eventlet.GreenPool()
    while True:
        try:
            new_sock, address = server.accept()
            print("accepted", address)
            pool.spawn_n(handle, new_sock.makefile('rw'))
        except (SystemExit, KeyboardInterrupt):
            break

def test_socket_connect():
    def geturl(url):
        c = socket.socket()
        ip = socket.gethostbyname(url)
        print('ip ', ip)
        c.connect((ip, 80))
        print('%s connected ' %url)
        c.sendall('GET /\r\n\r\n')
        return c.recv(1024)

    urls = ['www.python.org', 'www.baidu.com', 'www.hao123.com']
    pile = eventlet.GreenPile()
    for x in urls:
        # 产生一个绿色线程，调用geturl去处理x
        pile.spawn(geturl, x)
    for url, result in zip(urls, pile):
        print('%s : %s' %(url, repr(result)[:50]))

def test_multi_user_chat_server():
    PORT = 8090
    participants = set()

    def read_chat_forever(writer, reader):
        line = reader.readline()
        while line:
            print('Chat: ', line.strip())
            for p in participants:
                try:
                    if p is not writer:
                        p.write(line)
                        p.flush()
                except socket.error as e:
                    if e[0] != 32:
                        raise
            line =reader.readline()
        participants.remove(writer)
        print('Participant left chat.')
    try:
        print("ChatServer starting up on port %s" %PORT)
        server = eventlet.listen(('0.0.0.0', PORT))
        while True:
            new_conn, address = server.accept()
            print("Participant joined chat.")
            new_writer = new_conn.makefile('w')
            participants.add(new_writer)
            eventlet.spawn_n(read_chat_forever,
                             new_writer,
                             new_conn.makefile('r'))
    except (KeyboardInterrupt, SystemExit):
        print ('ChatServer exiting.')

def test_port_forwarder():
    def closed_callback():
        print('called back')

    def forward(source, dest, cb=lambda: None):
        while True:
            d = source.recv(32384)
            if d == '':
                cb()
                break
            dest.sendall(d)
    listener = eventlet.listen(('localhost', 8090))
    while True:
        client, addr = listener.accept()
        server = eventlet.connect(('localhost', 22))
        eventlet.spawn_n(forward, client, server, closed_callback)
        eventlet.spawn_n(forward, server, client)

def test_recursive_web_crawler():

    url_regex = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')


    def fetch(url, seen, pool):
        """Fetch a url, stick any found urls into the seen set, and
        dispatch any new ones to the pool."""
        print("fetching", url)
        data = ''
        with eventlet.Timeout(5, False):
            data = urllib2.urlopen(url).read()
        for url_match in url_regex.finditer(data):
            new_url = url_match.group(0)
            # only send requests to eventlet.net so as not to destroy the internet
            if new_url not in seen and 'baidu.com' in new_url:
                seen.add(new_url)
                # while this seems stack-recursive, it's actually not:
                # spawned greenthreads start their own stacks
                pool.spawn_n(fetch, new_url, seen, pool)


    def crawl(start_url):
        """Recursively crawl starting from *start_url*.  Returns a set of
        urls that were found."""
        pool = eventlet.GreenPool()
        seen = set()
        fetch(start_url, seen, pool)
        pool.waitall()
        return seen

    seen = crawl("http://baidu.com")
    print("I saw these urls:")
    print("\n".join(seen))

def test_producer_consumer_web_crawler():
    # http://daringfireball.net/2009/11/liberal_regex_for_matching_urls
    url_regex = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')


    def fetch(url, outq):
        """Fetch a url and push any urls found into a queue."""
        print("fetching", url)
        data = ''
        with eventlet.Timeout(5, False):
            data = urllib2.urlopen(url).read()
        for url_match in url_regex.finditer(data):
            new_url = url_match.group(0)
            outq.put(new_url)


    def producer(start_url):
        """Recursively crawl starting from *start_url*.  Returns a set of
        urls that were found."""
        pool = eventlet.GreenPool()
        seen = set()
        q = eventlet.Queue()
        q.put(start_url)
        # keep looping if there are new urls, or workers that may produce more urls
        while True:
            while not q.empty():
                url = q.get()
                # limit requests to eventlet.net so we don't crash all over the internet
                if url not in seen and 'eventlet.net' in url:
                    seen.add(url)
                    pool.spawn_n(fetch, url, q)
            pool.waitall()
            if q.empty():
                break

        return seen


    seen = producer("http://eventlet.net")
    print("I saw these urls:")
    print("\n".join(seen))

def test_websocket_server_example():
    @websocket.WebSocketWSGI
    def handle(ws):
        """  This is the websocket handler function.  Note that we
        can dispatch based on path in here, too."""
        if ws.path == '/echo':
            while True:
                m = ws.wait()
                if m is None:
                    break
                ws.send(m)

        elif ws.path == '/data':
            for i in six.moves.range(10000):
                ws.send("0 %s %s\n" % (i, random.random()))
                eventlet.sleep(0.1)


    def dispatch(environ, start_response):
        """ This resolves to the web page or the websocket depending on
        the path."""
        if environ['PATH_INFO'] == '/data':
            return handle(environ, start_response)
        else:
            start_response('200 OK', [('content-type', 'text/html')])
            return [open(os.path.join(
                         os.path.dirname(__file__),
                         'websocket.html')).read()]
    listener = eventlet.listen(('127.0.0.1', 8090))
    print("\nVisit http://localhost:7000/ in your websocket-capable browser.\n")
    wsgi.server(listener, dispatch)

def test_websocket_multi_user_chat_example():
    PORT = 8090
    participants = set()
    @websocket.WebSocketWSGI
    def handle(ws):
        participants.add(ws)
        try:
            while True:
                m = ws.wait()
                if m is None:
                    break
                for p in participants:
                    p.send(m)
        finally:
            participants.remove(ws)


    def dispatch(environ, start_response):
        """Resolves to the web page or the websocket depending on the path."""
        if environ['PATH_INFO'] == '/chat':
            return handle(environ, start_response)
        else:
            start_response('200 OK', [('content-type', 'text/html')])
            html_path = os.path.join(os.path.dirname(__file__), 'websocket_chat.html')
            return [open(html_path).read() % {'port': PORT}]


    # run an example app from the command line
    listener = eventlet.listen(('127.0.0.1', PORT))
    print("\nVisit http://localhost:7000/ in your websocket-capable browser.\n")
    wsgi.server(listener, dispatch)

def test_ssl():
    # insecure context, only for example purposes
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.set_verify(SSL.VERIFY_NONE, lambda *x: True)

    # create underlying green socket and wrap it in ssl
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = SSL.Connection(context, sock)

    # configure as server
    connection.set_accept_state()
    connection.bind(('127.0.0.1', 8443))
    connection.listen(50)

    # accept one client connection then close up shop
    client_conn, addr = connection.accept()
    print(client_conn.read(100))
    client_conn.shutdown()
    client_conn.close()
    connection.close()

if __name__ == '__main__':
    # test_web_crawler()
    # test_feed_scraper()
    # test_wsgi_server()
    # test_echo_server()
    # test_socket_connect()
    # test_multi_user_chat_server()
    # test_feed_scraper()
    # test_recursive_web_crawler()
    # test_producer_consumer_web_crawler()
    # test_websocket_server_example()
    # test_websocket_multi_user_chat_example()
    test_ssl()