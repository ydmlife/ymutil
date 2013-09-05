#!/usr/bin/env python
# encoding: utf-8
"""
emails.py

Copyright (c) 2012 qfpay Media. All rights reserved.
"""
import os
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


timestamp = time.strftime('%Y-%m-%d', time.gmtime(time.time() - 24 * 60 * 60))


def send_mail(smtpuser, smtppwd, fro, tolist, subject, text, files, smtpserver='smtp.qq.com', smtpport='', encode=None, html=False):
    """发带附件的邮件
    Args:
        smtpuser: 发件人邮箱
        smtppwd: 发件人密码
        fro: 发件人
        tolist: 收件人邮箱列表
        subject: 主题
        text: 正文
        files: 附件列表
        smtpserver: 邮件服务器
        smtpport: 邮件端口
    Returns:
    """
    assert type(tolist) == list
    assert type(files) == list
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(tolist)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header.Header(subject,"utf-8")
    if html:
        msg.attach(MIMEText(text,'html','utf-8'))
    else:
        msg.attach(MIMEText(text,'plain','utf-8'))
    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        Encoders.encode_base64(part)
        filename = os.path.basename(file)
        if encode:
            filename = filename.encode('gbk')
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
        msg.attach(part)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(smtpuser, smtppwd)
        smtp.sendmail(smtpuser, tolist, msg.as_string())
        smtp.quit()
        print fro,tolist,subject,text
        print "send suc"
    except Exception, e:
        print e, "send email failed"

def send_html_mail(to_list, mail_user, mail_pass, sub, context, mail_host='smtp.qq.com'):
    """发带正文为html的邮件
    Args:
        tolist: 收件人邮箱列表
        mail_user: 发件人邮箱
        mail_pass: 发件人密码
        sub: 主题
        context: html内容
        mail_host: 邮件服务器
    Returns:
    """
    msg = MIMEText(context, "html", "UTF-8")
    msg['Subject'] = sub
    msg['From'] = mail_user
    msg['To'] = ";".join(to_list)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host)
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(mail_user, to_list, msg.as_string())
        send_smtp.close()
        return True
    except Exception,e:
        print str(e), "the email send failure"
        return False


if __name__ == '__main__':
    pass


