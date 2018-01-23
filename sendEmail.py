#!/usr/bin/python
# -*- coding: UTF-8 -*-

#发送带附件邮件
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import traceback


def sendmail(Smtp_Server,Smtp_user,Smtp_password,Subject,TO=[],files=[]):
    # 实例
    msg = MIMEMultipart('alternative')
    msg['To'] = ';'.join(TO)
    msg['From'] = Smtp_user
    msg['Subject'] = Subject

    html = """\
    <html>
    <head><title>数字货币市值前一百名行情预览</title></head>
    <body>
    <p>数据来源于<a href="https://www.feixiaohao.com">非小号</a><br>
    点击进入<a href="http://www.along.party">蜷缩的蜗牛</a><br>
    </p>
    </body>
    </html>"""
    content = MIMEText(html, 'html', 'utf-8')
    msg.attach(content)

    # 构造附件，当多个为附件是用for读取构造
    for file in files:
        part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(Smtp_Server, 465)
        server.login(Smtp_user, Smtp_password)
        server.sendmail(Smtp_user, TO, msg.as_string())
        server.quit()
        message = 'Sendmail Success'
    except Exception, e:
        print str(e)
        message = traceback.format_exc()
    return message