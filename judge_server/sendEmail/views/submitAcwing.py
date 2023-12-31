from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

import time
import json
from websocket import create_connection


class webcket:
    def __init__(self, code, language, problem_id, cookie):
        self.url = "wss://www.acwing.com/wss/socket/"
        self.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Host": "www.acwing.com",
            "Origin": "https://www.acwing.com",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "Sec-WebSocket-Key": "R5Kb2hYHF7WRqepqchELkg==",
            "Sec-WebSocket-Version": "13",
            "Upgrade": "websocket",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Cookie": cookie,
        }
        self.code = code
        self.language = language
        self.problem_id = problem_id

    def connect(self):
        '''一直链接，直到连接上就退出循环'''
        while True:
            try:
                self.ws = create_connection(self.url, header=self.headers)
                # print(self.ws)
                break
            except Exception as e:
                print('连接异常：', e)
                continue

    def send_data(self):
        '''连接成功后，发送数据'''
        self.ws.send(json.dumps({
            "activity": "problem_submit_code",
            "problem_id": self.problem_id,
            "code": self.code,
            "language": self.language,
            "mode": "normal",
            "problem_activity_id": 0,
            "record": "[]",
            "program_time": 0}))  # 发送数据(必须为str类型)

    def run(self):
        '''执行，然后循环获取服务器返回的数据'''
        self.connect()
        self.send_data()
        time.sleep(1)
        while True:
            response = self.ws.recv()
            # print(f"结果：{response}")
            response = json.loads(response)
            if 'status' in response:
                if response['status'] != "ready" and response['status'] != "Pending" and response['status'] != "Judging":
                    self.ws.close()
                    return response['status']


def submitAcwing(request):
    data = request.POST
    code = data.get('code')
    language = data.get('language')
    problem_id = data.get('problem_id')
    cookie = data.get('cookie')
    res = None
    try:
        res = webcket(code, language, problem_id, cookie).run()
    except Exception as e:
        pass

    return HttpResponse(res)


if __name__ == '__main__':
    res = None
    try:
        res = webcket("123", "c++", "1001", "csrftoken=6gZS1z3PdR0Ilvuw3fU97ms5bFOm4cTnVS47XkUdnRT73KdMT8E0tH1brN9hmHqm; sessionid=2yf88rp8i6rwtyr4ha71960fbdedpfto").run()
    except Exception as e:
        pass
