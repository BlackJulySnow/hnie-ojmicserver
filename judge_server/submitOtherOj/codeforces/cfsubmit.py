import requests
import urllib3
import re
urllib3.disable_warnings()
# import certifi
# import cryptography
# import pyOpenSSL


def cfsubmit(contestId, id, lang, code, cookie):
    try:
        url = "https://codeforces.com/problemset/submit?csrf_token=" + cookie['csrf_token']
        headers = {
            "authority": "codeforces.com",
            "method": "POST",
            "path": "/problemset/submit?csrf_token=" + cookie['csrf_token'],
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "origin": "https://codeforces.com",
            "referer": "https://codeforces.com/problemset/submit",
            "upgrade-insecure-requests": "1",
            'Connection': 'close',
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
            "cookie": "JSESSIONID=" + cookie['JSESSIONID'] + "; X-User-Sha1=" + cookie['X_User_Sha1'] + ";",
        }
        data = {
            "csrf_token": cookie['csrf_token'],
            "bfaa": cookie['bfaa'],
            "action": "submitSolutionFormSubmitted",
            "contestId": contestId,
            "submittedProblemIndex": id,
            "programTypeId": lang,
            "source": code,
            "tabSize": "4",
        }
        res = requests.post(url=url, data=data, headers=headers, verify=False, timeout=10)
        s = res.text
        if s.find('<a href="/enter?back=%2F">Enter</a>') != -1:
            return {'result': 'false', 'msg': 'unlogin'}
        match = re.findall('submissionId="(.*?)"', s)
    except Exception as e:
        print(e)
        return {'result': 'false', 'msg': "提交时出现错误"}
    if len(match) == 0:
        match1 = re.findall('<span class="error for__source">(.*?)</span>', s)
        return {'result': 'false', 'msg': match1[0]}
    return {'result': 'true', 'submissionId': match[0]}


if __name__ == '__main__':
    res = cfsubmit('1722', 'D', '54', '#include <cstdio>', {"result": "true", "JSESSIONID": "B453DC5F778FC9FD4DCF1BE322D69BA7-n1", "X_User_Sha1": "a72c145eafcdddd1ef4a45cb1405b233bd3e87d0", "ftaa": "m107veb1ofp8ors2va", "bfaa": "0ed97987fd908a6f6f0c77f18469141f", "csrf_token": "1260b18b86c350fb900006c7a97d6a5d"})
    print(res)