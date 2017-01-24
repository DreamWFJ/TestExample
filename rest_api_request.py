# -*- coding: utf-8 -*-
import collections
import gzip
import urllib
import urllib2
from urlparse import urlparse

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import json
except ImportError:
    import simplejson as json


__author__ = 'myth'


_HTTP_GET = 1
_HTTP_POST = 2
# 超时时间（秒）
TIMEOUT = 45
RETURN_TYPE = {"json": 0, "xml": 1, "html": 2, "text": 3}
_METHOD_MAP = {'GET': _HTTP_GET, 'POST': _HTTP_POST}


class APIError(StandardError):
    """
    raise APIError if receiving json message indicating failure.
    """
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)


def _format_params(_pk=None, encode=None, **kw):
    """

    :param kw:
    :type kw:
    :param encode:
    :type encode:
    :return:
    :rtype:
    """

    __pk = '%s[%%s]' % _pk if _pk else '%s'
    encode = encode if encode else urllib.quote

    for k, v in kw.iteritems():
        _k = __pk % k
        if isinstance(v, basestring):
            qv = v.encode('utf-8') if isinstance(v, unicode) else v
            _v = encode(qv)
            yield _k, _v
        elif isinstance(v, collections.Iterable):
            if isinstance(v, dict):
                for _ck, _cv in _format_params(_pk=_k, encode=encode, **v):
                    yield _ck, _cv
            else:
                for i in v:
                    qv = i.encode('utf-8') if isinstance(i, unicode) else str(i)
                    _v = encode(qv)
                    yield _k, _v
        else:
            qv = str(v)
            _v = encode(qv)
            yield _k, _v


def encode_params(**kw):
    """
    do url-encode parameters

    >>> encode_params(a=1, b='R&D')
    'a=1&b=R%26D'
    >>> encode_params(a=u'u4e2du6587', b=['A', 'B', 123])
    'a=%E4%B8%AD%E6%96%87&b=A&b=B&b=123'

    >>> encode_params(**{
        'a1': {'aa1': 1, 'aa2': {'aaa1': 11}},
        'b1': [1, 2, 3, 4],
        'c1': {'cc1': 'C', 'cc2': ['Q', 1, '@'], 'cc3': {'ccc1': ['s', 2]}}
    })
    'a1[aa1]=1&a1[aa2][aaa1]=11&c1[cc1]=C&c1[cc3][ccc1]=s&c1[cc3][ccc1]=2&c1[cc2]=Q&c1[cc2]=1&c1[cc2]=%40&b1=1&b1=2&b1=3&b1=4'
    """
    # args = []
    # for k, v in kw.iteritems():
    #     if isinstance(v, basestring):
    #         qv = v.encode('utf-8') if isinstance(v, unicode) else v
    #         args.append('%s=%s' % (k, urllib.quote(qv)))
    #     elif isinstance(v, collections.Iterable):
    #         for i in v:
    #             qv = i.encode('utf-8') if isinstance(i, unicode) else str(i)
    #             args.append('%s=%s' % (k, urllib.quote(qv)))
    #     else:
    #         qv = str(v)
    #         args.append('%s=%s' % (k, urllib.quote(qv)))
    # return '&'.join(args)

    args = []
    _urlencode = kw.pop('_urlencode', urllib.quote)
    for k, v in _format_params(_pk=None, encode=_urlencode, **kw):
        args.append('%s=%s' % (k, v))

    args = sorted(args, key=lambda s: s.split("=")[0])
    return '&'.join(args)


def _read_body(obj):
    using_gzip = obj.headers.get('Content-Encoding', '') == 'gzip'
    body = obj.read()
    if using_gzip:
        gzipper = gzip.GzipFile(fileobj=StringIO(body))
        fcontent = gzipper.read()
        gzipper.close()
        return fcontent
    return body


class JsonDict(dict):
    """
        general json object that allows attributes to be bound to and also behaves like a dict
    """

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


def _parse_json(s):
    """
    parse str into JsonDict
    """

    def _obj_hook(pairs):
        """
        convert json object to python object
        """
        o = JsonDict()
        for k, v in pairs.iteritems():
            o[str(k)] = v
        return o
    return json.loads(s, object_hook=_obj_hook)


def _parse_xml(s):
    """
    parse str into xml
    """

    raise NotImplementedError()


def _parse_html(s):
    """
    parse str into html
    """

    raise NotImplementedError()


def _parse_text(s):
    """
    parse str into text
    """

    raise NotImplementedError()


def _http_call(the_url, method, return_type="json", request_type=None, request_suffix=None, headers={}, _timeout=30, **kwargs):
    """
    the_url: 请求地址
    method 请求方法（get，post）
    return_type： 返回格式解析
    request_suffix： 请求地址的后缀，如jsp，net
    _timeout: 超时时间
    kwargs: 请求参数
    """

    http_url = "%s.%s" (the_url, request_suffix) if request_suffix else the_url

    if request_type == 'json':
        headers['Content-Type'] = 'application/json'
        # method = _HTTP_POST
        # json_data = json.dumps(kwargs)
        # # convert str to bytes (ensure encoding is OK)
        # params = json_data.encode('utf-8')
        params = json.dumps(kwargs)
    else:
        params = encode_params(**kwargs)
        http_url = '%s?%s' % (http_url, params) if method == _HTTP_GET else http_url
    print http_url
    # u = urlparse(http_url)
    # headers.setdefault("host", u.hostname)
    http_body = None if method == _HTTP_GET else params

    req = urllib2.Request(http_url, data=http_body, headers=headers)

    callback = globals().get('_parse_{0}'.format(return_type))
    if not hasattr(callback, '__call__'):
        print "return '%s' unable to resolve" % return_type
        callback = _parse_json
    try:

        resp = urllib2.urlopen(req, timeout=_timeout if _timeout else TIMEOUT)
        body = _read_body(resp)
        r = callback(body)
        # if hasattr(r, 'error_code'):
        #     raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        return r
    except urllib2.HTTPError, e:
        try:
            body = _read_body(e)
            r = callback(body)
            return r
        except:
            r = None
        # if hasattr(r, 'error_code'):
        #     raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
            raise e


class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):

        def wrap(**kw):
            if attr:
                the_url = '%s/%s' % (self.client.api_url, attr.replace('__', '/'))
            else:
                the_url = self.client.api_url
            return _http_call(the_url, self.method, **kw)
        return wrap

    def __call__(self, **kw):
        return _http_call(self.client.api_url, self.method, **kw)


class APIClient(object):
    """
    使用方法：
        比如：api 请求地址为：http://api.open.zbjdev.com/kuaiyinserv/kuaiyin/billaddress
             请求方式为： GET
             需要的参数为：user_id 用户的UID
                         is_all 是否查询所有数据，0为默认邮寄地址 1为全部邮寄地址
                         access_token 平台认证
             返回数据为：json

        那么此时使用如下：
        domain = "api.open.zbjdev.com"
        #如果是https请求，需要将is_https设置为True
        client = APIClient(domain)
        data = {"user_id": "14035462", "is_all": 1, "access_token": "XXXXXXXXXX"}
        # 如果是post请求，请将get方法改为post方法
        result = client.kuaiyinserv.kuaiyin.billaddress.get(return_type="json", **data)
        #等同于
        # result = client.kuaiyinserv__kuaiyin__billaddress__get(return_type="json", **data)
        # result = client.kuaiyinserv__kuaiyin__billaddress(return_type="json", **data)
    """

    def __init__(self, domain, is_https=False):

        http = "http"
        if domain.startswith("http://") or domain.startswith("https://"):
            http, domain = domain.split("://")
        # else:
        if is_https:
            http = "https"

        self.api_url = ('%s://%s' % (http, domain)).rstrip("/")
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)

    def __getattr__(self, attr):
        if '__' in attr:

            method = self.get
            if attr[-6:] == "__post":
                attr = attr[:-6]
                method = self.post

            elif attr[-5:] == "__get":
                attr = attr[:-5]

            if attr[:2] == '__':
                attr = attr[2:]
            return getattr(method, attr)
        return _Callable(self, attr)


class _Executable(object):

    def __init__(self, client, method, path):
        self._client = client
        self._method = method
        self._path = path

    def __call__(self, **kw):
        method = _METHOD_MAP[self._method]
        return _http_call('%s/%s' % (self._client.api_url, self._path), method, **kw)

    def __str__(self):
        return '_Executable (%s %s)' % (self._method, self._path)

    __repr__ = __str__


class _Callable(object):

    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __getattr__(self, attr):
        if attr == 'get':
            return _Executable(self._client, 'GET', self._name)
        if attr == 'post':
            return _Executable(self._client, 'POST', self._name)
        name = '%s/%s' % (self._name, attr)
        return _Callable(self._client, name)

    def __str__(self):
        return '_Callable (%s)' % self._name

    __repr__ = __str__


def test_logistics():

    domain = "https://api.kuaidi100.com/api"

    #如果是https请求，需要将is_https设置为True
    client = APIClient(domain)

    data = {"id": "45f2d1f2sds", "com": "yunda", "nu": "1500066330925"}
    result = client.__get(_timeout=2, **data)
    print result
    print result["message"]
    print result.get("message")
    print result.message


if __name__ == '__main__':


    # test_logistics()

    data = {
        "data":{
            "id": 1,
            "pid": 3,
            "name": u'中的阿斯顿'
        },
        "sign": 'asdfdsdsfsdf',
    }

    domain = "kuaiyin.zhubajie.com"

    client = APIClient(domain)
    # headers = {'Content-Type': 'application/json'}
    headers = {"host": domain}

    result = client.api.zhubajie.fz.info.post(return_type="json", request_type="json", headers=headers, **data)
    print result
    print result['data']['msg']

    c = APIClient('task.6.zbj.cn')
    r = getattr(c.api, 'kuaiyin-action-delcache').post(request_type="json",
                                                       headers={},
                                                       **{"sign": "",
                                                          "data": {
                                                              "product": "pvc",
                                                              "category": "card",
                                                              "req_type": "pack_list"
                                                          }})
    print r
    print r['data']['msg']