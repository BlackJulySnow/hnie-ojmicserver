import requests


def csgGetInfo(RunID, cookie):
    url = "https://cpc.csgrandeur.cn/csgoj/Status/status_ajax"
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Host": "cpc.csgrandeur.cn",
        "Origin": "https://cpc.csgrandeur.cn",
        "Referer": "https://cpc.csgrandeur.cn/csgoj/status",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
    }
    params = {
        "sort": "solution_id_show",
        "order": "desc",
        "offset": "0",
        "limit": "20",
        "problem_id": "",
        "user_id": "",
        "solution_id": RunID,
        "language": "-1",
        "result": "-1",
    }
    res = requests.post(url=url, headers=headers, params=params).json()
    data = res['rows'][0]

    time = data['time']
    memory = data['memory']
    result = data['result']
    rate = data['pass_rate']
    return {'result': result, 'time': time, 'memory': memory, 'rate': rate}
