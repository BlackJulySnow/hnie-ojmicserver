import json
from datetime import datetime
from threading import Thread

from django.http import JsonResponse

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


def send_qqmail(content, receiver, code, count):
    # 第三方 SMTP 服务
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "acmore@hnieacm.com"  # 用户名
    mail_pass = "HNIEac666"  # 口令

    sender = 'acmore@hnieacm.com'
    receivers = []
    if count == 0:
        receivers.append(receiver)  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    else:
        for re in receiver:
            receivers.append(re)

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = formataddr(["ACMore", mail_user])

    if count == 0:
        message['To'] = formataddr(["", receiver])
    else:
        message['To'] = ','.join(receivers)

    subject = ''
    if code == 'acmore':
        subject = 'HNIEOJ'
    elif code == 'daka':
        subject = '打卡'
    elif code == 'tyy':
        subject = 'yyg'

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 465 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        if count == 0:
            smtpObj.sendmail(sender, receivers, message.as_string())
        else:
            smtpObj.sendmail(sender, message['To'].split(','), message.as_string())
        print("邮件发送成功 ")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件 ")


users = {
    'acmore': {},
    'tyy': {},
    'daka': {},
}


def sendEmail(request):
    data = request.POST
    code = data.get('code')
    content = data.get('content')
    receiver = data.get('email')
    count = data.get('count')
    receivers = data.get('receivers')
    # print(code)
    if not count is None:
        count = int(count)
    if code not in users:
        return JsonResponse({
            'result': "0",
            'msg': "无此用户",
        })
    now = datetime.now()

    if not count is None and count > 0:
        receivers = json.loads(receivers)
        # print(receivers)
        Thread(target=send_qqmail, args=(content, receivers, code, 1), daemon=True).start()
        return JsonResponse({
            'result': "1",
            'msg': "发送成功",
        })

    if receiver in users[code]:
        diff = now - users[code][receiver]
        if diff.total_seconds() <= 55:
            return JsonResponse({
                'result': "0",
                'msg': "相同邮件发送间隔小于60秒",
            })
    users[code][receiver] = now
    # print(users)
    Thread(target=send_qqmail, args=(content, receiver, code, 0), daemon=True).start()
    return JsonResponse({
        'result': "1",
        'msg': "发送成功",
    })


if __name__ == '__main__':
    send_qqmail("hhhh", "jilotus@qq.com", 1)
