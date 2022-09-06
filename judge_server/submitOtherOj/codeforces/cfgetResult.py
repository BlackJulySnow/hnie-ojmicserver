import requests
import urllib3
import re
urllib3.disable_warnings()
# import certifi
# import cryptography
# import pyOpenSSL


def cfgetResult(submissionId, cookie):
    url = "https://codeforces.com/data/submitSource"
    headers = {
        "authority": "codeforces.com",
        "method": "POST",
        "path": "/data/submitSource",
        "scheme": "https",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "origin": "https://codeforces.com",
        "referer": "https://codeforces.com/problemset/status?my=on",
        "upgrade-insecure-requests": "1",
        "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "XMLHttpRequest",
        "x-csrf-token": cookie['csrf_token'],
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
        "cookie": "JSESSIONID=" + cookie['JSESSIONID'] + "; X-User-Sha1=" + cookie['X_User_Sha1'] + ";",
    }
    data = {
        "csrf_token": cookie['csrf_token'],
        "submissionId": submissionId,
    }
    res = requests.post(url=url, data=data, headers=headers, verify=False, timeout=30).json()
    if res['waiting'] == 'true':
        print(res['waiting'])
        return {'result': 'false', 'msg': 'waiting'}
    print(res['verdict'])
    return {'result': "true", 'verdict': res['verdict']}


if __name__ == '__main__':
    flag = False
    resq = None
    for i in range(0, 10):
        try:
            resq = cfgetResult('170450659')
            flag = resq['result']
        except Exception as e:
            pass
        if flag:
            break
    print(resq)
