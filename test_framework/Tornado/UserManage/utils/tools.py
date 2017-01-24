# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : tools.py
# CreateTime    : 2016-09-19 22:54
# ==================================

from uuid import uuid4
import base64
import random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AESCBC():
    def __init__(self, key='ThisAESCBCciphy!', mode=AES.MODE_CBC, key_length=16):
        self.key = key
        self.mode = mode
        self.key_lenght = key_length

    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        count = len(text)
        add = self.key_lenght - (count % self.key_lenght)
        text = text + ('\0' * add)
        cipher_text = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串，再base64转码
        return base64.encodestring(b2a_hex(cipher_text))

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(base64.decodestring(text)))
        return plain_text.rstrip('\0')


def get_uuid():
    return str(uuid4())

def range_string(length=16, region="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789="):
    return ''.join([random.choice(region) for _ in xrange(length)])


cipher_hander = AESCBC()
range_cipher_handler = AESCBC(range_string(), key_length=32)

