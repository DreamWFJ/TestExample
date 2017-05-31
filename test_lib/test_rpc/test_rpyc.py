# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_rpyc.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-31 9:52
# ===================================
import rpyc
from rpyc import Service
from rpyc.utils.server import ThreadedServer
import os

class Test(Service):
    def exposed_cmd(self, cmd):
        return os.system(cmd)

def test_server():
    sr = ThreadedServer(Test, port=9999, auto_register=False)
    sr.start()

def test_client():
    conn = rpyc.connect('localhost', 9999)
    cr = conn.root.cmd('ls')
    conn.close()



if __name__ == '__main__':
    # test_server()
    test_client()
