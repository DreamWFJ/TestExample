# -*- coding: utf-8 -*-
# ===================================
# ScriptName : checkout.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-21 9:31
# ===================================

import re

def regex_test(msg, pattern):
    regex = re.compile(pattern)
    result = regex.match(msg)
    if result:
        return True
    else:
        return False

def checkout_uuid(uuid):
    uuid_pattern = r'[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}'
    return regex_test(uuid, uuid_pattern)


def checkout_username(username):
    username_pattern = r'^[a-zA-Z][\w_]{4,12}[a-zA-Z]$'
    return regex_test(username, username_pattern)




def checkout_password(password):
    '''
    :Note - 密码长度必须在6-32位之间，必须包含数字，大小写字母和这些特殊字符 '!@#$%^&*_+-='

    :param password:
    :return:
    '''
    special_char = '!@#$%^&*_+-='
    number = '0123456789'
    captial_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_case_char = 'abcdefghijklmnopqrstuvwxyz'

    def test_in_string(destination_str, assign_string):
        for i in assign_string:
            if i in destination_str:
                return True
        return False

    for s in [
        special_char,
        number,
        captial_char,
        lower_case_char
    ]:
        if not test_in_string(password, s):
            return False

    password_pattern = r'[\w!@#$%^&*_+-=]{6,32}'
    return regex_test(password, password_pattern)








from tools import range_string

def test_username():
    region="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    for i in [
        range_string(8, region) for _ in range(10)
    ]:
        print i, checkout_username(i)


def test_password():
    region="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*_+-="
    for i in [
        range_string(8, region) for _ in range(10)
    ]:
        print i, checkout_password(i)

    for i in [
        'ABC12345',
        'aBc-adsf123',
        '123123',
        '1a-Af',
        '123234345345',
        'adsfasdfasdf',
        'ADSFASDFJALSDF',
        'ASDFfasdf13123',
        'Abc-123123234'
    ]:
        print i, checkout_password(i)

if __name__ == '__main__':
    test_password()
    