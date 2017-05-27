# -*- coding: utf-8 -*-
# ===================================
# ScriptName : crawler_proxy_ip.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-26 9:05
# ===================================

import requests
from bs4 import BeautifulSoup as bs
import re
import time
import threading

lock = threading.Lock()
def proxy_list(mbUrl):
    headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"}
    url='http://www.xicidaili.com/nn/'
    r = requests.get(url=url, headers=headers)
    soup = bs(r.content)
    datas=soup.find_all(name='tr',attrs={'class':re.compile('|[^odd]')})
    datalen=len(datas)
    threads=[] #定义一个线程队列
    ip = []
    port = []
    types = []
    for i in range(datalen):
        soup_proxy_content=bs(str(datas[i]))
        soup_proxys=soup_proxy_content.find_all(name='td')
        ip.append(str(soup_proxys[1].string))
        port.append(str(soup_proxys[2].string))
        types.append(str(soup_proxys[5].string))
    for i in range(datalen):
        t=threading.Thread(target=proxy_test,args=(mbUrl,ip[i],port[i],types[i],))
        threads.append(t)
    for i in range(datalen):
        threads[i].start()
        #time.sleep(0.2)
    for i in range(datalen):
        threads[i].join()

def proxy_test(url, ip, port, types):
    proxy={}
    proxy[types.lower()]='%s:%s'%(ip,port)
    try:
        r=requests.get(url,proxies=proxy,timeout=3) #会把每个代理ip都测试一遍，超时设置为六秒
        ip_content=re.findall(r'\[(.*?)\]',r.text)[0]#匹配[]中的ip
        if ip==ip_content:#判断代理是否测试成功
            lock.acquire()  # 线程锁
            print proxy
            lock.release()
    except Exception,e:
        #print e
        pass
def test_threading():
    time_start = time.time()
    proxy_list("http://1212.ip138.com/ic.asp")
    time_finished=time.time()-time_start
    print time_finished

if __name__ == '__main__':
    test_threading()
    