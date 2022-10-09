import requests
import urllib3
import re
urllib3.disable_warnings()
# import certifi
# import cryptography
# import pyOpenSSL


def cfgetResult(submissionId, cookie):
    url = "https://codeforces.com/data/submitSource"
    try:
        headers = {
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
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
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
        }
        data = {
            "csrf_token": cookie['csrf_token'],
            "submissionId": submissionId,
        }
        res = requests.post(url=url, data=data, headers=headers, verify=False, timeout=60).json()
    except Exception as e:
        print(e)
        return {'result': 'false', 'mag': "获取结果时错误"}
    if res['waiting'] == 'true':
        print(res['waiting'])
        return {'result': 'false', 'msg': 'waiting'}
    print(res['verdict'])

    testCount = res['testCount']
    count = int(testCount)
    info = ""
    for i in range(1, count + 1):
        k = str(i)
        info += "\n======================================================================="
        info += "\n" + "Test: #" + k + ", time: " + res['timeConsumed#'+k] + \
                "ms, memory: " + res['memoryConsumed#'+k] + "B, exit code: " + \
                res['exitCode#'+k] + ", checker exit code: " + res['checkerExitCode#'+k] + \
                ", verdict: " + res['verdict#'+k] + "\n"
        info += "\n" + "Input" + "\n"
        info += res['input#'+k]
        info += "\n" + "Output" + "\n"
        info += res['output#'+k]
        info += "\n" + "Answer" + "\n"
        info += res['answer#'+k]
        info += "\n" + "Checker Log" + "\n"
        info += res['checkerStdoutAndStderr#'+k] + "\n"
        info += "=======================================================================\n"

    return {'result': "true", 'verdict': res['verdict'], 'info': info}


if __name__ == '__main__':
    flag = False
    resq = None
    for i in range(0, 10):
        try:
            resq = cfgetResult('175202997', {"result": "true", "JSESSIONID": "501148A914FD245BFC1F5F7A4FE5A418-n1", "X_User_Sha1": "a72c145eafcddff1ef4a45cb1405b233bd3e87d0", "ftaa": "m107vea1ofp8ors2va", "bfaa": "0ed96987fd908a6f6f0c77f18469141f", "csrf_token": "6d23a9b457659e668eb8c4f62854257d"})
            flag = resq['result']
        except Exception as e:
            print(e)
        if flag:
            break
    print(resq)
