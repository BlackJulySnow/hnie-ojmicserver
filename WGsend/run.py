import json

import requests

from MysqlUtil import MysqlUtil


def sendNoneDo():
    db = MysqlUtil()
    users = db.queryAllUserEmail()
    db.closeMysql()
    content = "今天自动晚归打卡因未知因素开摆了，快上易班晚归打卡。（若已自己打卡请忽略）"
    receivers = []
    for user in users:
        receivers.append(user['email'])
    print(receivers)
    if len(receivers) > 0:
        datas = {
            'code': "daka",
            'content': content,
            'count': len(receivers),
            'receivers': json.dumps(receivers),
        }
        url = "http://127.0.0.1:8000/sendEmail/"
        res = requests.post(url=url, data=datas)
        print(res.text)


if __name__ == '__main__':
    sendNoneDo()
