from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


def send_qqmail(content, receiver):
    # 第三方 SMTP 服务
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "acmore@hnieacm.com"  # 用户名
    mail_pass = "HNIEac666"  # 口令

    sender = 'acmore@hnieacm.com'
    receivers = receiver  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = formataddr(["ACMore", mail_user])
    message['To'] = formataddr(["", receiver])

    subject = 'HNIEOJ'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 465 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功 ")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件 ")


def sendEmail(request):
    data = request.POST
    code = data.get('code')
    content = data.get('content')
    receiver = data.get('email')

    if code != "acmore":
        return JsonResponse({
            'result': "0",
            'msg': "错误",
        })
    send_qqmail(content, receiver)
    return JsonResponse({
        'result': "1",
    })


if __name__ == '__main__':
    send_qqmail("hhhh", "jilotus@qq.com")
