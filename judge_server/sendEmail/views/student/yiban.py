import requests
import hashlib


class yiban:
    def __init__(self, username, password, JSESSIONID, num):
        self.username = username
        self.password = 'Hnie@' + password
        self.num = num
        self.cookies = None
        self.toke = ""
        self.JSESSIONID = JSESSIONID
        self.getPwMd5()

    def setProxies(self, proxies):
        self.proxies = proxies

    def getPwMd5(self):
        pwd = self.password.encode(encoding='utf-8')
        m = hashlib.md5()
        m.update(pwd)
        pwd = m.hexdigest()
        if len(pwd) > 5:
            pwd = pwd[0:5] + "a" + pwd[5:len(pwd)]

        if len(pwd) > 10:
            pwd = pwd[0:10] + "b" + pwd[10:len(pwd)]

        pwd = pwd[0:len(pwd) - 2]
        self.password = pwd

    def getTokenFromStr(self, s):
        i = s.find("zzdk_token") + 10
        s = s[i:]
        i = s.find("value") + 7
        s = s[i:i + 6]
        # print(str)
        return s

    def getToken(self):
        try:
            url = "http://xggl.hnie.edu.cn/wap/menu/student/temp/zzdk/_child_/edit"
            heard = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Cookie": "JSESSIONID=" + self.JSESSIONID,
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 Edg/103.0.1264.62",
                "Referer": "http://xggl.hnie.edu.cn/wap/menu/student/temp/zzdk?_t_s_=" + self.num,
                "Host": "xggl.hnie.edu.cn",
            }
            params = {
                '_t_s_': self.num,
            }
            res = requests.get(url, params=params, headers=heard, timeout=20).text
        except Exception as e:
            return False
        self.toke = self.getTokenFromStr(res)
        return True

    def getJSESSIONID(self):
        url = "http://xggl.hnie.edu.cn/index"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Host": "xggl.hnie.edu.cn",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 Edg/103.0.1264.62",
        }
        try:
            res = requests.get(url, headers=headers, timeout=20)
            self.JSESSIONID = requests.utils.dict_from_cookiejar(res.cookies)['JSESSIONID']
        except Exception as e:
            # print(e)
            pass

    def signUp(self):
        self.getJSESSIONID()
        url = "http://xggl.hnie.edu.cn/website/login"
        params = {
            'uname': self.username,
            'pd_mm': self.password,
        }
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Host": "xggl.hnie.edu.cn",
            "Origin": "http://xggl.hnie.edu.cn",
            "Referer": "http://xggl.hnie.edu.cn/index",
            "Cookie": "JSESSIONID=" + str(self.JSESSIONID),
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 Edg/103.0.1264.62",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            res = requests.post(url=url, params=params, headers=headers, timeout=20)
            # self.cookies = requests.utils.dict_from_cookiejar(res.cookies)
            # print(res.text)
            index_url = res.json()['goto2']
            # print("密码正确，成功登陆")
            self.num = index_url[-13:]
        except Exception as e:
            # if 'error' in res:
            # print(e)
            return {"result": False, "msg": "密码错误"}
        print(self.JSESSIONID)
        return {"result": True, "msg": "登录成功"}

    def get_stu_info(self, user_id):
        url = "http://xggl.hnie.edu.cn/content/tabledata/student/studentbase/query?" \
              "sEcho=3&iColumns=10&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=12" \
              "&mDataProp_0=0&bSortable_0=false&mDataProp_1=XH&bSortable_1=true&mDataProp_2=XM&bSortable_2=true" \
              "&mDataProp_3=XB_MC&bSortable_3=true&mDataProp_4=BJMC&bSortable_4=true&mDataProp_5=MZ_MC&bSortable_5=true" \
              "&mDataProp_6=SYSF&bSortable_6=true&mDataProp_7=7&bSortable_7=false&mDataProp_8=SFZX&bSortable_8=true&mDataProp_9=XJZT" \
              "&bSortable_9=true&iSortCol_0=4&sSortDir_0=asc&iSortCol_1=1&sSortDir_1=asc&iSortingCols=2&nj=&xh=" + str(user_id) + "&yxb=&zy=" \
              "&bj=&sfzx=1&xjzt=1&mz=&sysf=&zzmm=&xb=&fdy=&_=1668141019887&_t_s_=" + self.num
        # print(url)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Host": "xggl.hnie.edu.cn",
            "Origin": "http://xggl.hnie.edu.cn",
            "Referer": "http://xggl.hnie.edu.cn/content/menu/student/studentbase/query/mgr?_t_s_=" + self.num,
            "Cookie": "JSESSIONID=" + str(self.JSESSIONID),
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 Edg/103.0.1264.62",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            res = requests.get(url=url, headers=headers).json()
            # print(res)
            res = res['aaData'][0]
        except Exception as e:
            print(e)
            if e == "list index out of range":
                return None
            else:
                return "unlogin"
        return {
            "user_id": res['XH'],
            "school": res['BJMC'],
            "nick": res['XM'],
        }
