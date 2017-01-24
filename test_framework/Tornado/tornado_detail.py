# -*- coding: utf-8 -*-
# ===================================
# ScriptName : tornado_detail.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-19 13:32
# ===================================

import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web


'''
class tornado.web.RequestHandler(application, request, **kwargs)
    基本的请求类

# --- 装饰 ---
tornado.web.asynchronous(method)
    例如：实现异步请求，在3.1版本之后，用@gen.coroutine
    class MyRequestHandler(RequestHandler):
        @asynchronous
        def get(self):
           http = httpclient.AsyncHTTPClient()
           http.fetch("http://friendfeed.com/", self._on_download)

        def _on_download(self, response):
           self.write("Downloaded!")
           self.finish()
# 用户装饰登录认证的方法
tornado.web.authenticated(method)

# 为请求的url添加反斜杠
tornado.web.addslash(method)

# 为请求的url移除反斜杠
tornado.web.removeslash(method)

# 为RequestHandler子类开启streaming body支持
tornado.web.stream_request_body(cls)

# --- 一切别的东西 ---
exception tornado.web.HTTPError(status_code=500, log_message=None, *args, **kwargs)
exception tornado.web.Finish
exception tornado.web.MissingArgumentError(arg_name)
class tornado.web.UIModule(handler)
    render(*args, **kwargs)
    embedded_javascript()
    javascript_files()
    embedded_css()
    css_files()
    html_head()
    html_body()
    render_string(path, **kwargs)

class tornado.web.ErrorHandler(application, request, **kwargs)
    # 为所有的请求根据错误码产生一个错误响应
class tornado.web.FallbackHandler(application, request, **kwargs)
    # 一个装饰另外一个HTTP服务回调的RequestHandler
    例如：
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    application = tornado.web.Application([
        (r"/foo", FooHandler),
        (r".*", FallbackHandler, dict(fallback=wsgi_app),
    ])

class tornado.web.RedirectHandler(application, request, **kwargs)
    # 将所有的GET请求重定向到指定的URL

class tornado.web.StaticFileHandler(application, request, **kwargs)
    例如：
    application = web.Application([
        (r"/content/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
    ])

# -------------------------- tornado.template -- 灵活的输出产生

基本用法
    t = template.Template("<html>{{ myvalue }}</html>")
    print t.generate(myvalue="XXX")

    loader = template.Loader("/home/btaylor")
    print loader.load("test.html").generate(myvalue="XXX")


class tornado.template.Template(template_string, name="<string>", loader=None, compress_whitespace=None, autoescape="xhtml_escape", whitespace=None)
class tornado.template.BaseLoader(autoescape='xhtml_escape', namespace=None, whitespace=None)
class tornado.template.Loader(root_directory, **kwargs)
class tornado.template.DictLoader(dict, **kwargs)
exception tornado.template.ParseError(message, filename=None, lineno=0)
tornado.template.filter_whitespace(mode, text)

# ---------------------------- tornado.escape -- 转义
# ---------------------------- tornado.locale -- 国际化支持
# ---------------------------- tornado.websocket -- 与浏览器双向通信
class tornado.websocket.WebSocketHandler(application, request, **kwargs)
    例如：
    class EchoWebSocket(tornado.websocket.WebSocketHandler):
        def open(self):
            print("WebSocket opened")

        def on_message(self, message):
            self.write_message(u"You said: " + message)

        def on_close(self):
            print("WebSocket closed")
    浏览器中JS
    var ws = new WebSocket("ws://localhost:8888/websocket");
    ws.onopen = function() {
       ws.send("Hello, world");
    };
    ws.onmessage = function (evt) {
       alert(evt.data);
    };


'''

# 全局配置文件设置
# tornado.options.parse_config_file('config.ini')

class MainHandler(tornado.web.RequestHandler):
    # 子类初始化钩子，每个请求都会调用，这里的参数是从url中来
    def initialize(self, database=None):
        self.database = database

    # 在一个get/post请求之前调用，可以使用gen.coroutine, return_futrue, asynchronous去装饰，实现异步
    def prepare(self):
        pass

    # 在一个请求结束后调用
    def on_finish(self):
        pass

    # 添加额外的METHOD
    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS + ('PROPFIND',)

    def propfind(self):
        pass

    def get(self, *args, **kwargs):
        # ----------- 输入 -------------
        # 请求处理程序可以通过 self.request 访问到代表当前请求的对象。该 HTTPRequest 对象包含了一些有用的属性，包括：
        #
        # arguments - 所有的 GET 或 POST 的参数
        # files - 所有通过 multipart/form-data POST 请求上传的文件
        # path - 请求的路径（ ? 之前的所有内容）
        # headers - 请求的开头信息
        # 从参数中以name获取参数值，没有则取默认值，无默认值则抛出MissingArgumentError异常
        name = self.get_argument('name', default=None)
        # 同上，只是这里返回的是列表
        name_list = self.get_arguments('name')

        # 从请求的查询字符串中获取参数，没有则取默认值，无默认值则抛出MissingArgumentError异常
        query_string = self.get_query_argument('name', default=None)
        # 同上，只是这里返回的是列表
        query_string_list = self.get_query_arguments('name')

        # 从请求body中获取参数
        body_args = self.get_body_argument('name', default=None)
        # 同上，只是这里返回的是列表
        body_args_list = self.get_body_arguments('name')

        # 从请求中解码参数
        decode_args = self.decode_argument('aa', name=None)

        # 包含额外的请求参数在headers和body数据中
        extra_args = self.request

        # 传递给METHOD的关键参数
        path_args = self.path_args
        path_kwargs = self.path_kwargs

        # 长传的文件可以通过如下方式访问到，对象名称为html元素<input type='file'>的name属性对应到一个文件列表。每一个文件都以字典的形式 存在，其格式为 {"filename":..., "content_type":..., "body":...}。
        # self.request.files
        # 如果你想要返回一个错误信息给客户端，例如“403 unauthorized”，只需要抛出一个 tornado.web.HTTPError 异常：

        # if not self.user_is_logged_in():
        #     raise tornado.web.HTTPError(403)

        #------------- 输出 -------------
        # 设置响应状态码
        self.set_status('404', reason='not found page')
        # 设置头信息
        self.set_header('TEST', 'TEST')
        # 添加头信息
        self.add_header('TSET', 'TEST')
        # 清除头信息
        self.clear_header('TEST')
        # 设置默认头信息
        self.set_default_headers()

        # 将给的块信息写入到输出中
        self.write("Hello, world")

        # 将当前输出缓存刷新到网络
        self.flush()

        # 关闭响应，终止HTTP请求
        self.finish()

        # 作为响应参数渲染模板
        self.render(template_name='index.html', kwargs={'test':'test'})
        self.render_string(template_name='index.html', kwargs={'test':'test'})

        # 返回一个字典，用于模板的默认命名空间
        self.get_template_namespace()

        # 发送一个重定向到指定的URL
        self.redirect('http://www.baidu.com', permanent=False)

        # 发送错误码到浏览器
        self.send_error(status_code=500)

        # 重写错误页面
        self.write_error(status_code=500)

        # 重置响应头和内容
        self.clear()

        # 处理流请求数据
        data = self.data_received()


        # ---------- Cookies -----------
        all_cookies = self.cookies

        # 获取指定的cookies
        v = self.get_cookie('name', default=None)

        # 设置cookies选项值
        self.set_cookie('name', 'value', domain=None, expires=10, path='/', expires_days=None)
        # 清除cookies
        self.clear_cookie('name', path='/', domain=None)
        self.clear_all_cookies(path='/', domain=None)
        # 获取签字的cookies
        self.get_secure_cookie('name', value=None, max_age_days=31, min_version=None)
        # 获取安全的签字密钥cookie版本
        self.get_secure_cookie_key_version('name', value=None)
        self.set_secure_cookie('name', 'value', expires_days=30, version=None)
        # 签字和时间戳
        value = self.create_signed_value('name', 'value', version=None)
        # 设置签字版本
        tornado.web.MIN_SUPPORTED_SIGNED_VALUE_VERSION = 1
        tornado.web.MAX_SUPPORTED_SIGNED_VALUE_VERSION = 2
        tornado.web.DEFAULT_SIGNED_VALUE_MIN_VERSION = 1
        tornado.web.DEFAULT_SIGNED_VALUE_VERSION = 2



        # -------- 其它 ------------
        # 应用对象，可以通过它获取内部属性
        application = self.application

        # 检查Etag头
        self.check_etag_header()
        # 设置Etag头
        self.set_etag_header()
        # 检查xsrf
        self.check_xsrf_cookie()
        # 计算etag头
        self.compute_etag()

        # 从给定的路径返回一个新的模板
        p = self.create_template_loader('/path/template/index.html')

        # 请求中的认证用户
        user = self.current_user

        # 获取访问的浏览器位置
        self.get_browser_locale(default='en_US')

        # 获取当前用户, 可以重写
        self.get_current_user()

        # 获取登录URL, 可以重写
        self.get_login_url()

        # 获取响应状态
        self.get_status()

        # 获取模板路径
        self.get_template_path()

        # 获取认证用户的位置，可以重写
        self.get_user_locale()

        # session中的locale
        locale = self.locale

        # 重写未捕获的日志异常
        self.log_exception(IOError, '1', 1)

        # 如果客户关闭连接，使用的异步调用句柄
        self.on_connection_close()

        # 如果给定的APP未定义，则抛出异常
        self.require_setting('name', feature='this feuture')

        # Application.reverse_url的别名
        self.reverse_url('name')

        # self.application.settings的别名
        settings = self.settings

        # 根据给定的相对静态文件路径返回一个静态URL
        url = self.static_url('/test/www', include_host=None)

        self.xsrf_form_html()
        token = self.xsrf_token



    def head(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        pass

class ArticleHandler(tornado.web.RequestHandler):
    pass

if __name__ == "__main__":
    # 这里是支持配置文件的
    tornado.options.parse_command_line()
    # Application(handlers=None, default_host='', transforms=None, **settings)
    application = tornado.web.Application([
        (r"/test/(.*)", MainHandler, dict(database=database)),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/var/www"}),
    ])
    # add_handlers(host_pattern, host_handlers)
    application.add_handlers(r"www\.myhost\.com", [
        (r"/article/([0-9]+)", ArticleHandler),
    ])
    # 监听给定的端口
    application.listen(8888)

    # reverse_url('name', *args)
    # log_request(handler) --将一个完整的请求写入日志中
    '''
    settings = {
        # 当文件被改变时，自动重载服务
        autoreload = True,
        debug = True
        compiled_template_cache=Flase
        static_hash_cache = False
        serve_traceback=True
        # 用于未匹配的方法的处理，比如404
        default_handler_class
        default_handler_args
        # gzip在4.0之后不用了，用下面的代替
        compress_response = True
        # Application.log_request 重写，用于日志
        log_function = '日志句柄'
        ui_modules
        ui_methods

        cookie_secrt
        key_version

        login_url
        xsrf_cookies
        xsrf_cookie_version
        xsrf_cookie_kwargs
        twitter_consumer_key, twitter_consumer_secret, friendfeed_consumer_key, friendfeed_consumer_secret, google_consumer_key, google_consumer_secret, facebook_api_key, facebook_secret

        # --- template settings ---
        autoescape
        compiled_template_cache
        template_path
        template_loader
        template_whitespace
        # --- static file settings ---
        static_hash_cache
        static_path
        static_url_prefix
        static_handler_class, static_handler_args

    }

    # ----------- tornado.httpserver ---- 非阻塞HTTP服务，单线程
    class tornado.httpserver.HTTPServer(*args, **kwargs)
    # ssl
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.path.join(data_dir, "mydomain.crt"),
                            os.path.join(data_dir, "mydomain.key"))
    HTTPServer(applicaton, ssl_options=ssl_ctx)

    单线程处理
        server = HTTPServer(app)
        server.listen(8888)
        IOLoop.current().start()

    多线程处理
        server = HTTPServer(app)
        server.bind(8888)
        server.start(0)  # Forks multiple sub-processes
        IOLoop.current().start()

    高级多线程处理
        sockets = tornado.netutil.bind_sockets(8888)
        tornado.process.fork_processes(0)
        server = HTTPServer(app)
        server.add_sockets(sockets)
        IOLoop.current().start()

    class tornado.httpclient.HTTPClient(async_client_class=None, **kwargs)
        例如：
        http_client = httpclient.HTTPClient()
        try:
            response = http_client.fetch("http://www.google.com/")
            print response.body
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))
        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))
        http_client.close()

    class tornado.httpclient.AsyncHTTPClient
        例如：
        def handle_response(response):
            if response.error:
                print "Error:", response.error
            else:
                print response.body

        http_client = AsyncHTTPClient()
        http_client.fetch("http://www.google.com/", handle_response)

    class tornado.httpclient.HTTPRequest(url, method='GET', headers=None, body=None, auth_username=None, auth_password=None, auth_mode=None, connect_timeout=None, request_timeout=None, if_modified_since=None, follow_redirects=None, max_redirects=None, user_agent=None, use_gzip=None, network_interface=None, streaming_callback=None, header_callback=None, prepare_curl_callback=None, proxy_host=None, proxy_port=None, proxy_username=None, proxy_password=None, allow_nonstandard_methods=None, validate_cert=None, ca_certs=None, allow_ipv6=None, client_key=None, client_cert=None, body_producer=None, expect_100_continue=False, decompress_response=None, ssl_options=None)
    class tornado.httpclient.HTTPResponse(request, code, headers=None, buffer=None, effective_url=None, error=None, request_time=None, time_info=None, reason=None)
    exception tornado.httpclient.HTTPError(code, message=None, response=None)
    class tornado.simple_httpclient.SimpleAsyncHTTPClient
    class tornado.curl_httpclient.CurlAsyncHTTPClient(io_loop, max_clients=10, defaults=None)





    '''

    tornado.ioloop.IOLoop.current().start()