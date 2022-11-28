# 导入库
import urllib.request
import bs4
from bs4 import BeautifulSoup
from django.http import JsonResponse


def getCfProblem(request):
    data = request.GET
    # 题目属性
    # problemSet = "1736"
    # problemId = "A"
    problemSet = data.get('problemSet')
    problemId = data.get('problemId')

    cid = int(problemSet)
    # 题目链接
    if cid < 100000:
        url = f"https://codeforces.com/problemset/problem/{problemSet}/{problemId}"
    else:
        url = f"https://codeforces.com/gym/{problemSet}/problem/{problemId}"
    # 获取网页内容
    html = urllib.request.urlopen(url).read()
    # 格式化
    soup = BeautifulSoup(html,'lxml')

    # 存储
    data_dict = {'Note': ""}
    # 找到主体内容
    mainContent = soup.find_all(name="div", attrs={"class" :"problem-statement"})[0]

    # Limit
    # 找到题目标题、时间、和内存限制
    # Title
    data_dict['Title'] = mainContent.find_all(name="div", attrs={"class":"title"})[0].contents[-1]
    # Time Limit
    data_dict['Time Limit'] = mainContent.find_all(name="div", attrs={"class":"time-limit"})[0].contents[-1]
    # Memory Limit
    data_dict['Memory Limit'] = mainContent.find_all(name="div", attrs={"class":"memory-limit"})[0].contents[-1]


    def divTextProcess(div):
        """
        处理<div>标签中<p>的文本内容
        """
        strBuffer = ''
        # 遍历处理每个<p>标签
        for each in div.find_all("p"):
            for content in each.contents:
                # 如果不是第一个，加换行符
                if (strBuffer != ''):
                    strBuffer += '\n\n'
                # 处理
                if (type(content) != bs4.element.Tag):
                # 如果是文本，添加至字符串buffer中
                    strBuffer += "<p>" + content.replace("       ", " ").replace("$$$", "$") + "</p>"
                else:
                # 如果是html元素，如span等，加上粗体
                    strBuffer += "<p>" + "**" + content.contents[0].replace("       ", " ").replace("$$$", "$") + "**" + "</p>"
        # 返回结果
        return strBuffer


    # 处理题目描述
    data_dict['Problem Description'] = divTextProcess(mainContent.find_all("div")[10])

    div = mainContent.find_all(name="div", attrs={"class":"input-specification"})[0]
    data_dict['Input'] = divTextProcess(div)

    div = mainContent.find_all(name="div", attrs={"class":"output-specification"})[0]
    data_dict['Output'] = divTextProcess(div)

    # Input
    div = mainContent.find_all(name="div", attrs={"class":"input"})[0]
    pre = div.find_all("pre")[0]
    data_dict['Sample Input'] = ""
    l = len(pre.find_all("div"))
    for i in range(l):
        data_dict['Sample Input'] += pre.find_all("div")[i].contents[0] + "\n"
    # Onput
    div = mainContent.find_all(name="div", attrs={"class":"output"})[0]
    data_dict['Sample Output'] = div.find_all("pre")[0].contents[0]
    # data_dict['Sample Output'] = data_dict['Sample Output'][2:]

    # 若有样例说明
    if (len(mainContent.find_all(name="div", attrs={"class": "note"})) > 0):
        div = mainContent.find_all(name="div", attrs={"class": "note"})[0]
        data_dict['Note'] = divTextProcess(div)

    data_dict['Source'] = '[' + data_dict['Title'] + ']' + '(' + url + ')'

    for each in data_dict.keys():
        # print('### ' + each + '\n')
        s = data_dict[each].replace("</p>\n\n<p>**", "<strong>").replace("**</p>\n\n<p>", "</strong>").replace("\leq", "<=").replace("\\times", "×").replace("\dots", "...")
        l = s.find('$')
        while l != -1:
            r = s[l + 1:].find('$') + l + 1
            s = s[:l] + "<b>" + s[l + 1:r] + "</b>" + s[r + 1:]
            l = s.find('$')
        l = s.find('^')
        while l != -1:
            if s[l + 1] == '{':
                r = s[l + 1:].find('}') + l + 1
                s = s[:l] + "<sup>" + s[l + 2:r] + "</sup>" + s[r + 1:]
            else:
                s = s[:l] + "<sup>" + s[l + 1] + "</sup>" + s[l + 2:]
            l = s.find('^')
        l = s.find('_')
        while l != -1:
            if s[l + 1] == '{':
                r = s[l + 1:].find('}') + l + 1
                s = s[:l] + "<sub>" + s[l + 2:r] + "</sub>" + s[r + 1:]
            else:
                s = s[:l] + "<sub>" + s[l + 1] + "</sub>" + s[l + 2:]
            l = s.find('_')
        data_dict[each] = s
        # print(s)

    return JsonResponse({
        "Title": data_dict['Title'],
        "Time_Limit": data_dict['Time Limit'].replace(" seconds", "").replace(" second", ""),
        "Memory_Limit": data_dict['Memory Limit'].replace(" megabytes", ""),
        "Problem_Description": data_dict['Problem Description'],
        "Input": data_dict['Input'],
        "Output": data_dict['Output'],
        "Sample_Input": data_dict['Sample Input'],
        "Sample_Output": data_dict['Sample Output'],
        "Note": data_dict['Note'],
        "Source": data_dict['Source'],
    })


if __name__ == '__main__':
    res = getCfProblem(1)
    print(res)
