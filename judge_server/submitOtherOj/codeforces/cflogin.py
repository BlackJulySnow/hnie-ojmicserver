import requests
import urllib3
import re
urllib3.disable_warnings()
# import certifi
# import cryptography
# import pyOpenSSL

ftaas = ['', '', '', '', '', '', '', '', '', 'dhjypfwev3g20rx4fo', 'm107vea1ofp8ors2va', 'am9gg9ww3h541sbe5p']
bfaas = ['', '', '', '', '', '', '', '', '', '748390a84a22d8f4e9b56ff73b8d9aed', '0ed96987fd908a6f6f0c77f18469141f', '20cede18901b680d11fc6e47c5f355e0']


def getToken(session):
    url = "https://codeforces.com/enter"
    headers = {
        "authority": "codeforces.com",
        "method": "GET",
        "path": "/enter",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "origin": "https://codeforces.com",
        "referer": "https://codeforces.com/enter",
        "upgrade-insecure-requests": "1",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
    }
    res = requests.get(url=url, headers=headers, verify=False, timeout=30)
    s = res.text
    csrf_token = re.findall('<meta name="X-Csrf-Token" content="(.*?)"/>', s)[0]
    return {'csrf_token': csrf_token}


def codeforcesLogin(username, password, ftaa, bfaa, csrf_token, session):
    url = "https://codeforces.com/enter"
    headers = {
        "authority": "codeforces.com",
        "method": "POST",
        "path": "/enter",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "origin": "https://codeforces.com",
        "referer": "https://codeforces.com/enter",
        "upgrade-insecure-requests": "1",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
    }
    data = {
        "csrf_token": csrf_token,
        "action": "enter",
        "ftaa": ftaa,
        "bfaa": bfaa,
        "handleOrEmail": username,
        "password": password,
        "_tta": "745",
    }
    session.post(url=url, data=data, headers=headers, verify=False, timeout=30)


def cflogin(username, password, ojId):
    session = requests.session()
    ftaa = ftaas[ojId]
    bfaa = bfaas[ojId]
    res = None
    flag = True
    for i in range(0, 10):
        try:
            res = getToken(session)
            codeforcesLogin(username, password, ftaa, bfaa, res['csrf_token'], session)
            if session.cookies.get('X-User-Sha1', default=False):
                flag = False
                break
        except Exception as e:
            pass
    if flag:
        return {'result': 'false'}
    cookies = session.cookies
    return {
        'result': 'true',
        'JSESSIONID': cookies.get('JSESSIONID'),
        'X_User_Sha1': cookies.get('X-User-Sha1'),
        'ftaa': ftaa,
        'bfaa': bfaa,
        'csrf_token': res['csrf_token']
    }
