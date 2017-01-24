# -*- coding: utf-8 -*-
# ===================================
# ScriptName : crawler.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-27 11:22
# ===================================
"""
汉王 23.0
福特 3.0
绿盟 33.0
启明 20.5
可立克 27.0
中航三鑫 10.0
红旗连锁 7.0
"""

import random
import datetime
import time
import urllib2
import smtplib
from email.mime.text import MIMEText
from email.header import Header

USER_AGENT = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv',
    'Mozilla/5.0 (Windows NT 6.1; rv',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
]

def get_stock_price(stock_code, stock_exchange='sz'):
    # 深圳证券 sz
    # 上海证券 sh
    url = "http://hq.sinajs.cn/list=" + "%s%s"%(stock_exchange, stock_code)
    req = urllib2.Request(url)
    req.add_header("User-Agent", random.choice(USER_AGENT))
    response = urllib2.urlopen(req)
    content = response.read()
    data = content.decode("gb2312")
    data_tuple = data.split(',')
    stock_name = data_tuple[0].split('"')[1]
    current_price = data_tuple[3]
    current_date = "%s %s"%(data_tuple[30], data_tuple[31])
    print current_date, stock_name, current_price
    return current_price

def detect_stock_price(stock_name, stock_code,  max_price=21.20, min_price=20.50, stock_exchange='sz'):
    is_send_email = False
    now = datetime.datetime.now()
    hour = float("%s.%s"%(now.hour, now.minute if len(str(now.minute)) > 1 else "0%d"%now.minute))
    if (hour >= 9.30 and hour <= 11.30) or (hour >= 13.00 and hour <= 15.00):
        msg = ""
        current_price = get_stock_price(stock_code)
        if float(current_price) > max_price:
            is_send_email = True
            msg = u"+++ 股票: '%s', 代码: '%s', 当前价格 << '%s' >> 已经高于预定义卖出价格: -- '%s' --, 可以出手"%(stock_name, stock_code, current_price, str(max_price))
        if float(current_price) < min_price:
            is_send_email = True
            msg = u"--- 股票: '%s', 代码: '%s', 当前价格 << '%s' >> 已经低于预定义购买价格: -- '%s' --, 可以出手"%(stock_name, stock_code, current_price, str(max_price))
        if is_send_email:
            send_email("wfj_sc@126.com", "wfj_sc@126.com", u"股票价格提示", msg)
    elif (hour > 15.00 and hour < 23.59) or (hour > 0.00 and hour < 9.30):
        print u"股市关闭阶段..."
        is_send_email = True

    return is_send_email

def send_email(fr, to, subject, body):
    msg = MIMEText(body,'text','utf-8')#中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect('smtp.126.com')
    smtp.login("wfj_sc@126.com", "abc123")
    smtp.sendmail(fr, to, msg.as_string())
    smtp.quit()



def timer_task():
    # u'启明星辰', u'002439', max_price=23.00
    while not detect_stock_price(u'汉王科技', u'002362', max_price=24.00):
        time.sleep(300)
if __name__ == '__main__':
    timer_task()
    