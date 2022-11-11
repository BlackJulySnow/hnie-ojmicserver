import requests
import urllib3
import re
urllib3.disable_warnings()
# import certifi
# import cryptography
# import pyOpenSSL


def cfgetMessage(submissionId, cookie, contestId):
    cid = int(contestId)
    if cid < 100000:
        url = "https://codeforces.com/problemset/status?my=on"
        referer = "https://codeforces.com/problemset/status?my=on"
    else:
        url = "https://codeforces.com/gym/" + str(contestId) + "/my"
        referer = "https://codeforces.com/gym/" + str(cid) + "/submit?csrf_token=" + cookie['csrf_token']
    try:
        headers = {
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            "authority": "codeforces.com",
            "method": "GET",
            "path": "/problemset/status?my=on",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": 'gzip, deflate, br',
            "origin": "https://codeforces.com",
            "referer": referer,
            "upgrade-insecure-requests": "1",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
            "cookie": "JSESSIONID=" + cookie['JSESSIONID'] + "; X-User-Sha1=" + cookie['X_User_Sha1'] + ";",
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
        }
        res = requests.get(url=url, headers=headers, verify=False, timeout=60)
    except Exception as e:
        print(e)
        return {'result': 'false', 'mag': "获取信息时错误", 'time': '1', 'space': '1000'}
    s = res.text
    # print(s)

    # match0 = re.findall('submissionId="(.*?)"', s)
    # if match0[0] != submissionId:
    #     return {'result': "false", 'time': '1', 'space': '1000'}
    match = re.findall('(.*?)&nbsp;ms', s)
    match1 = re.findall('(.*?)&nbsp;KB', s)
    time = match[0].replace(' ', '')
    space = match1[0].replace(' ', '')
    return {'result': 'true', 'time': time, 'space': space}


if __name__ == '__main__':
    flag = False
    resq = None
    for i in range(0, 10):
        try:
            resq = cfgetMessage('178668553', {"result": "true", "JSESSIONID": "4BF1F31BB01AD7D7ED7C5CDDE9300A7C-n1", "X_User_Sha1": "9ee9673b6cc183716ec33547728fe6d18b1ba898", "ftaa": "dhjypfwev3g20rx4fo", "bfaa": "748390a84a22d8f4e9b56ff73b8d9aed", "csrf_token": "ae0ade363b59b9897d859f2fddf24694"}
                                , "104008")
            flag = resq['result']
        except Exception as e:
            pass
        if flag:
            break
    print(resq)
