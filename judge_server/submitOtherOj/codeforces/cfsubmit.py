import requests
import urllib3
import re
urllib3.disable_warnings()
# import certifi
# import cryptography
# import pyOpenSSL


def getsubmissionId(cookie, cid):
    if cid < 100000:
        url = "https://codeforces.com/problemset/status?my=on"
        referer = "https://codeforces.com/problemset/status?my=on"
    else:
        url = "https://codeforces.com/gym/" + str(cid) + "/my"
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
        return {'result': 'false', 'mag': "获取提交id失败"}
    s = res.text
    match0 = re.findall('submissionId="(.*?)"', s)
    return {'result': 'true', 'submissionId': match0[0]}


def cfsubmit(contestId, id, lang, code, cookie, username):
    cid = int(contestId)
    try:
        if cid < 100000:
            url = "https://codeforces.com/problemset/submit?csrf_token=" + cookie['csrf_token']
            referer = "https://codeforces.com/problemset/submit"
        else:
            url = "https://codeforces.com/gym/" + str(contestId) + "/submit?csrf_token=" + cookie['csrf_token']
            referer = "https://codeforces.com/gym/" + str(contestId) + "/submit?csrf_token=" + cookie['csrf_token']
        headers = {
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'accept-encoding': 'gzip, deflate, br',
            "authority": "codeforces.com",
            "method": "POST",
            "path": "/problemset/submit?csrf_token=" + cookie['csrf_token'],
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
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
        res = requests.post(url=url, data=data, headers=headers, verify=False, timeout=60)
        s = res.text
        # print(s)
        if s.find('<a href="/enter?back=%2F">Enter</a>') != -1:
            return {'result': 'false', 'msg': 'unlogin'}
        match = []
        if cid < 100000:
            match = re.findall('submissionId="(.*?)"', s)
        if len(match) == 0 and cid < 100000:
            match1 = re.findall('<span class="error for__source">(.*?)</span>', s)
            return {'result': 'false', 'msg': match1[0]}
        # match1 = re.findall('user-black">(.*?)</a>', s)
        # user = match1[0]
        # print(str(user) + " " + str(username))
        # submissionId = match[0]
        # if user != username:
        flag = False
        resq = None
        submissionId = ""
        for i in range(0, 10):
            try:
                resq = getsubmissionId(cookie, cid)
                flag = resq['result']
            except Exception as e:
                pass
            if flag == "true":
                submissionId = resq['submissionId']
                print(submissionId)
                break
        return {'result': 'true', 'submissionId': submissionId}
    except Exception as e:
        print(e)
        return {'result': 'false', 'msg': "提交时出现错误"}


if __name__ == '__main__':
    res = cfsubmit("104008", "A", "54", "#include \"bits/stdc++.h\"\r\n\r\n\r\nconst int N = 100010;\r\n\r\nint main() {\r\n    int t;\r\n    cin >> t;\r\n    while(t --) {\r\n        int n, status[N],cnti = 0, cntf = 0;\r\n        long long ice[N], fire[N];\r\n        scanf(\"%d\", &n);\r\n        for(int i = 0; i < n; i ++ )\r\n            scanf(\"%d\", &status[i]);\r\n        for(int i = 0; i < n; i ++ )\r\n            if(status[i] == 0) {\r\n                scanf(\"%d\", &ice[cnti]);\r\n                cnti ++;\r\n            }\r\n            else {\r\n                scanf(\"%d\", &fire[cntf]);\r\n                cntf++;\r\n            }\r\n\r\n        sort(ice,ice + cnti);\r\n        sort(fire, fire + cntf);\r\n\r\n        long long ans = 0;\r\n        if(cnti < cntf) {\r\n            int j = cntf - 1;\r\n           for(int i = 0; i < cnti; i ++ )\r\n               ans += (2 * ((long long)fire[j--] + ice[i]));\r\n           while(j >= 0)\r\n               ans += fire[j--];\r\n        }\r\n        else if(cnti == cntf) {\r\n            if(ice[0] < fire[0])\r\n                ans += ice[0] + 2 * fire[0];\r\n            else\r\n                ans += fire[0] + 2 * ice[0];\r\n            for(int i = 1; i < cnti; i ++ )\r\n                ans += 2 * (fire[i] + ice[i]);\r\n        }\r\n        else {\r\n            int j = cnti - 1;\r\n            for(int i = 0; i < cntf; i ++)\r\n                ans += (2 * (ice[j--] + fire[i]));\r\n            while(j >= 0)\r\n                ans += ice[j--];\r\n        }\r\n        printf(\"%lld\\n\", ans);\r\n    }\r\n\r\n    return 0;\r\n}\r\n",
             {"result": "true", "JSESSIONID": "D106803B13FCFC94C6F99225DD8048E9-n1", "X_User_Sha1": "a2860f13e6950e253d9bf2841220bde962e85e87", "ftaa": "am9gg9ww3h541sbe5p", "bfaa": "20cede18901b680d11fc6e47c5f355e0", "csrf_token": "01349fdec96f8236b98045b2ee15b5e4"}, "hnie3")
    # res = getsubmissionId({"result": "true", "JSESSIONID": "D106803B13FCFC94C6F99225DD8048E9-n1", "X_User_Sha1": "a2860f13e6950e253d9bf2841220bde962e85e87", "ftaa": "am9gg9ww3h541sbe5p", "bfaa": "20cede18901b680d11fc6e47c5f355e0", "csrf_token": "01349fdec96f8236b98045b2ee15b5e4"}
    #                       , 104008)
    print(res)