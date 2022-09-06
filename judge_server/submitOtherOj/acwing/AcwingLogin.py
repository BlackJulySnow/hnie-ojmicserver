import requests
import re


def AcwingLogin(username, password):
    res = requests.get(url="https://www.acwing.com")
    s = res.text
    mathch = re.findall(r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)">', s)

    csrftoken = mathch[0]
    login_url = "https://www.acwing.com/user/account/signin/"
    data = {
        "csrfmiddlewaretoken": csrftoken,
        "username": username,
        "password": password,
        "remember_me": "on",
    }
    headers = {
        "Cookie": "csrftoken=" + csrftoken,
        "sec-ch-ua": 'Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Host": "www.acwing.com",
        "Origin": "https://www.acwing.com",
        "Referer": "https://www.acwing.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
    }
    res = requests.post(url=login_url, data=data, headers=headers)
    cookie = dict(res.cookies)
    s = "csrftoken=" + cookie['csrftoken'] + "; sessionid=" + cookie['sessionid']
    return s
