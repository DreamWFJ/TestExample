# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : cookie_count.py
# CreateTime    : 2016-09-16 18:38
# ==================================

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1

        countString = "1 time" if count == 1 else "%d times" % count

        self.set_secure_cookie("count", str(count))

        self.write(
            '<html><head><title>Cookie Counter</title></head>'
            '<body><h1>You’ve viewed this page %s times.</h1>' % countString +
            '</body></html>'
        )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    # >>> import base64, uuid
    # >>> base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    # 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E='
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        # CSRF/XSRF
        # <form action="/purchase" method="POST">
        #     {% raw xsrf_form_html() %}
        #     <input type="text" name="title" />
        #     <input type="text" name="quantity" />
        #     <input type="submit" value="Check Out" />
        # </form>

        # JS中的设置
        # function getCookie(name) {
        #     var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        #     return c ? c[1] : undefined;
        # }
        #
        # jQuery.postJSON = function(url, data, callback) {
        #     data._xsrf = getCookie("_xsrf");
        #     jQuery.ajax({
        #         url: url,
        #         data: jQuery.param(data),
        #         dataType: "json",
        #         type: "POST",
        #         success: callback
        #     });
        # }
        "xsrf_cookies": True
    }

    application = tornado.web.Application([
        (r'/', MainHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()