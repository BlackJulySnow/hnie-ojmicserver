import requests
import re


def AcwingGetInfo(id, cookie):
    try:
        url = "https://www.acwing.com/problem/content/submission/" + str(id) + "/"
        header = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Host": "www.acwing.com",
            "Referer": url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
            "Cookie": cookie,
        }
        res = requests.get(url=url, headers=header)
        s = res.text
        mathch = re.findall(r'<a href="/problem/content/submission/code_detail/(.*?)/">', s)
        sid = mathch[0]

        url = "https://www.acwing.com/problem/content/submission/code_detail/" + str(sid) + "/"
        header = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Host": "www.acwing.com",
            "Referer": url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
            "Cookie": cookie,
        }
        res = requests.get(url=url, headers=header)
        s = res.text
        # print(s)
        mathch = re.findall(r'<span>(.*?)</span>', s)
        data = str(mathch[0]).split('/')
        passdata = data[0]
        alldata = data[1]
        time = mathch[1]
        space = mathch[2]
        rate = round(int(passdata) / int(alldata), 2)
    except Exception as e:
        print(e)
        return {'result': False}

    return {'result': True, "rate": rate, "time": time, "space": space}
