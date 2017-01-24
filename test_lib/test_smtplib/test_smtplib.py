# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

HOST = "smtp.126.com"
PASSWORD = "abc123"
SUBJECT = 'test'
FROM = "wfj_sc@126.com"
TO = "wangfangjie@pdmi.cn"

def addimg(src, imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage

def add_attach(attach_path, show_attach_name):
    attach = MIMEText(open(attach_path, "rb").read(), "base64", "utf-8")
    attach["Content-Type"] = "application/octet-stream"
    attach_name = "attachment; filename=\"%s\""%show_attach_name
    attach_name = attach_name.decode("utf-8").encode("gb18030")
    attach["Content-Disposition"] = attach_name
    return attach

def send_mail(e_from, e_password, e_to, e_msg, e_host, e_port="25"):
    try:
        server = smtplib.SMTP()
        server.connect(e_host, e_port)
        server.starttls()
        server.login(e_from, e_password)
        server.sendmail(e_from, e_to, msg.as_string())
        server.quit()
        print "发送邮件成功!"
    except Exception, e:
        print "失败："+str(e)

msg = MIMEMultipart('related')
# s = "<font color=red>wfj test 邮件:<br><img src=\"cid:weekly\" border=\"1\"><br>详细说明见附件。</font>"
s = "test"
msg_text = MIMEText(s, "html", "utf-8")
msg.attach(msg_text)
msg.attach(addimg("img/weekly.png", "weekly"))

msg.attach(add_attach("doc/week_report.xlsx", "周报.xlsx"))
msg["Subject"] = SUBJECT
msg["To"] = TO
msg["From"] = FROM
send_mail(FROM, PASSWORD, TO, msg, HOST)