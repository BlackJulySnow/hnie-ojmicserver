import requests


def csgLogin(username, password, cookie):
    url = "https://cpc.csgrandeur.cn/csgoj/user/login_ajax"
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Host": "cpc.csgrandeur.cn",
        "Origin": "https://cpc.csgrandeur.cn",
        "Referer": "https://cpc.csgrandeur.cn/csgoj/user/userinfo?user_id=" + str(username),
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
    }
    data = {
        "user_id": username,
        "password": password,
    }
    res = requests.post(url=url, data=data, headers=headers).json()
    print(res)
    if res['msg'] == "Login successful!<br/>Reloading data." or res['msg'] == "User already logged in. Try refreshing the page.":
        return True
    else:
        return False
