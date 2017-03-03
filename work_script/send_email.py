# -*- coding: utf-8 -*-
# ===================================
# ScriptName : send_email.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-03 15:59
# ===================================

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
#Read_File
file_read = open('/root/Data_File.txt','r')
f=file_read.read()
#Mail_Define
from_addr = 'menchao@we.com'
password = '2345132412'
to_addr = ["menchao@we.com", "zhangxu@we.com"]
smtp_server = '10.20.22.19'
msg = MIMEText(f, 'plain', 'utf-8')
#msg['From'] = _format_addr(u'离职人员清单 <%s>' % from_addr)
#msg['To'] = _format_addr(u'请各位同学知晓 <%s>' % to_addr)
msg['Subject'] = Header(u'来自IT管理部_本周离职人员清单', 'utf-8').encode()

#Send_Mail
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()
    