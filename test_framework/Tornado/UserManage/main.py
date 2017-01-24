# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : main.py
# CreateTime    : 2016-09-16 21:45
# ==================================
import os.path
import logging
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import json
import traceback
from tornado.web import url
from tornado.options import options, define
import pymongo
from utils.tools import get_uuid
from bson.objectid import ObjectId
from utils.tools import cipher_hander
from UserException.exception import InvalidJson, InvalidUsername, InvalidPhoneNum, InvalidRequestArgs, RWMongoDBError


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
logger = logging.getLogger(__file__)

define('port', default=8000, help='run on the given port', type=int)
define('debug', default=True, help='run in debug mode', type=bool)


'''
用户管理平台
    设计理念：RESTFul框架的用户管理平台，实现用户的注册，登录，登出，修改信息，为用户绑定角色信息，关联权限信息，不同协议验证接口（OAuth1,2）
    后端数据库采用mongo实现，使用tornado异步框架
'''

UUID_REGEX = '[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}'

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.application.user_cache
        self.write('current user cache info: %'%json.dumps(data))
    def write_error(self, status_code, **kwargs):
        self.write('Gosh darnit, user! You caused a %d error.' %status_code)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if username and password:
            session_id = get_uuid()
            self.write('login, session id : %s'%session_id)
            self.application.user_cache[session_id] = (username, password)
        else:
            raise u'认证失败'

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        self.write('logout')

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class AlterDetailHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class UserManagerHandler(tornado.web.RequestHandler):
    '''
        GET /version/user/{user_id} -- show
        PUT /version/user/{user_id} -- update
        DELETE /version/user/{user_id} -- delete
        GET /version/user -- list
        POST /version/user -- create
        POST /version/user -- bulk create
    '''
    def initialize(self, user_id=None):
        self.user_id = user_id

    def prepare(self):
        # 试试tornado的异步链接
        db = self.application.conn['UserManage']
        self.collection_name = db['user']

    def on_finish(self):
        conn = self.application.conn
        conn.close()


    def get(self , user_id=None):
        '''
        功能：查询用户或者获取用户信息列表
        :param user_id:
        :return:
        '''
        if user_id:
            query_result = self.collection_name.find_one({"user_id":user_id}, {"_id":0, "password":0})
            # del query_result["_id"]
            # del query_result["password"]
        else:
            # db.Account.find().sort("UserName",pymongo.ASCENDING)   --升序
            # db.Account.find().sort("UserName",pymongo.DESCENDING)  --降序
            # query_result = self.collection_name.find().limit(1).skip(10).sort("username", pymongo.ASCENDING)
            query_result = self.collection_name.find(None, {"_id":0, "password":0}).sort("username", pymongo.DESCENDING)
            if query_result:
                query_result = json.dumps(list(query_result))
        print query_result
        self.write(query_result)

    def is_invalid_username(self, username):
        # 查询为空时返回None
        if not username:
            return True
        result = self.collection_name.find_one({'username':username})
        return bool(result)

    def is_invalid_phone_number(self, phone_number):
        # 查询为空时返回None
        if not phone_number:
            return True
        result = self.collection_name.find_one({'phone_number':phone_number})
        return bool(result)



    def post(self, *args, **kwargs):
        '''
            调用命令：curl -l -H "Content-type: application/json" -X POST -d '{"phone_number":"13521389587","password":"test","username":"wfj"}' http://127.0.0.1:8000/version/user
            功能：创建新用户调用的接口
        '''
        try:
            try:
                request_args = json.loads(self.request.body)
            except Exception, e:
                raise InvalidJson("Invalid request, please check json format.")

            if not request_args or not isinstance(request_args, (dict, list)):
                raise InvalidRequestArgs()
            insert_condition = None
            faild_list = []

            def make_insert_data(args):
                username = args.get('username', None)
                password = args.get('password', None)
                phone_number = args.get('phone_number', None)
                user_id = get_uuid()
                if self.is_invalid_phone_number(phone_number):
                    msg = 'phone number "%s" has been existed, please input again.' %phone_number
                    raise InvalidPhoneNum(msg)
                if self.is_invalid_username(username):
                    msg = 'username "%s" has been existed, please input again.' %username
                    raise InvalidUsername(msg)
                if not password:
                    raise Exception("in parameters, 'password' must be filled.")
                result_dict = {
                    "user_id": user_id,
                    "username": username,
                    "password": cipher_hander.encrypt(password),
                    "phone_number": phone_number,
                }
                return result_dict

            if isinstance(request_args, list):
                insert_condition = list()
                print request_args
                for one in request_args:
                    try:
                        print "1-----", type(one), one
                        data = make_insert_data(one)
                        insert_condition.append(data)
                    except Exception, e:
                        logger.warning(traceback.print_exc())
                print "insert_condition: ", type(insert_condition), insert_condition
                if len(insert_condition) == 0:
                    raise InvalidRequestArgs("please check request parameters, they have been existed.")

            if isinstance(request_args, dict):
                insert_condition = make_insert_data(request_args)
            # self.set_header('Content-Type', 'application/json')
            #--------------------------- 注意 -------------------------- 这里最好对数据库操作方法进行封装一下，包裹异常
            # 写入数据
            object_ids =  self.collection_name.insert(insert_condition)
            if object_ids and isinstance(object_ids, ObjectId):
                self.write(insert_condition)
            elif object_ids and isinstance(object_ids, list) and len(object_ids)<=len(insert_condition) and len(object_ids) > 0:
                self.write({"success":insert_condition})
            else:
                raise RWMongoDBError()

        except Exception, e:
            msg = str(e)
            logger.error(msg)
            print type(e)
            self.write(msg)
        # json_dict = {'user_id':user_id, 'username':username,'password':password, 'phone_num':phone_num}
        # self.write(json.dumps(json_dict))

    def patch(self, user_id=None):
        '''
        功能：更新某一条信息
        :param args:
        :param kwargs:
        :return:
        '''
        pass

    def put(self, user_id=None):
        '''
        功能：更新用户信息（多条）
        :param user_id:
        :return:
        '''
        try:
            try:
                request_args = json.loads(self.request.body)
            except Exception, e:
                raise InvalidJson("Invalid request, please check json format.")

            if not request_args or not isinstance(request_args, dict):
                raise InvalidRequestArgs()
            update_condition = None
            faild_list = []

            def make_update_data(args):
                # 以下字段参考的百度
                username = args.get('username', None)
                sex = args.get('sex', None)
                birthday = args.get('birthday', None)
                blood_type = args.get('')
                # 身份证号
                identity_card_number = ""
                email_address = ""
                qq_number = ""
                weixin_number = ""
                birth_place = ""
                #居住地
                place_of_residence = ""
                # 个人简介
                personal_profile = ""
                # 体型
                bodily_form = ""
                # 婚姻状态
                marital_status = ""
                # 教育程度
                degree_of_education = ""
                # 教育背景
                educational_background = [{"学校类型":"大学", "学校名称":"北京大学", "入学年份":"2010-10.6"}]
                # 职业
                prefession = ""
                # 工作单位信息
                work_unit = [{"工作单位":"xxx","工作起止时间":"2010/11/3-2014/5/5"}]
                # 头像
                head_portrait = "保存固定大小的16进制编码"


                result_dict = {
                    "sex": sex,
                    "username": username,
                    "birthday": birthday,
                    "blood_type": blood_type,
                    "identity_card_number":identity_card_number,
                    "email_address":email_address,
                    "qq_number":qq_number,
                    "weixin_number":weixin_number,
                    "birth_place":birth_place,
                    "place_of_residence":place_of_residence,
                    "personal_profile":personal_profile,
                    "bodily_form":bodily_form,
                    "marital_status":marital_status,
                    "degree_of_education":degree_of_education,
                    "educational_background":educational_background,
                    "prefession":prefession,
                    "work_unit":work_unit,
                    "head_portrait":head_portrait,
                }
                return result_dict


            if isinstance(request_args, dict):
                update_condition = make_update_data(request_args)
            # self.set_header('Content-Type', 'application/json')
            #--------------------------- 注意 -------------------------- 这里最好对数据库操作方法进行封装一下，包裹异常
            # 更新数据
            object_ids =  self.collection_name.update({"user_id":user_id}, update_condition)
            if object_ids and isinstance(object_ids, ObjectId):
                self.write(update_condition)
            else:
                raise RWMongoDBError()

        except Exception, e:
            msg = str(e)
            logger.error(msg)
            print type(e)
            self.write(msg)

    def delete(self, user_id=None):
        '''
        功能：删除用户信息
        :param user_id:
        :return:
        '''
        if user_id:
            result = self.collection_name.delete_one({"user_id":user_id})
            print type(result), result
            self.write("delete user_id: '%s' success."%user_id)
        else:
            self.write("'user_id' must be existed.")


class UserManagerApplication(tornado.web.Application):
    def __init__(self):
        # url格式
        '''
        GET /version/user/{user_id} -- show
        PUT /version/user/{user_id} -- update
        DELETE /version/user/{user_id} -- delete
        GET /version/user -- list
        POST /version/user -- create
        POST /version/user -- bulk create
        请求和返回都是Json格式
        '''

        handlers = [
            url(r"/version", IndexHandler),
            url(
                # 该url可以匹配如下地址
                # /version/user
                # /version/user/
                # /version/user/123456
                r"/version/user(?:/)?(?P<user_id>%s)?"%UUID_REGEX,
                UserManagerHandler,
                dict(user_id=None),
                name='user'
            )
        ]
        # handlers = [
        #     (r'/', IndexHandler),
        #     (r'/user/login', LoginHandler),
        #     (r'/user/logout', LogoutHandler),
        #     (r'/user/register', RegisterHandler),
        #     (r'/user/alter', AlterDetailHandler),
        # ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=True,
            debug = options.debug,
        )
        self.conn = pymongo.MongoClient('localhost', 27017)

        self.user_cache = dict()
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(UserManagerApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    # tornado.ioloop.IOLoop.instance().start()