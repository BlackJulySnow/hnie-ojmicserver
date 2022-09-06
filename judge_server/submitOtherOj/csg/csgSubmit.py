import requests


def csgSubmit(pid, code, lang, cookie):
    url = "https://cpc.csgrandeur.cn/csgoj/Problemset/submit_ajax"
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Host": "cpc.csgrandeur.cn",
        "Origin": "https://cpc.csgrandeur.cn",
        "Referer": "https://cpc.csgrandeur.cn/csgoj/problemset/submit?pid=" + str(pid),
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
    }
    data = {
        "language": lang,
        "pid": pid,
        "source": code,
    }
    res = requests.post(url=url, headers=headers, data=data).json()
    print(res)
    if res['msg'] == "Please Login First!":
        return None
    elif res['msg'] == "Submit successful! <br/>Redirecting to Status.":
        return res['data']['solution_id']
    else:
        return None
