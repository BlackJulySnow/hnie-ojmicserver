from cflogin import login
from submit import submit
from cfgetResult import getResult
from cfgetMessage import getMessage


res = login('hnie1', 'Hnieacm')
print(res)
resp = submit(res['csrf_token'], res['bfaa'], res['JSESSIONID'], res['X-User-Sha1'])
if resp['result'] is False:
    print(resp['msg'])
    exit(0)

submissionId = resp['submissionId']

flag = False
resp = None
for i in range(0, 10):
    try:
        resp = getResult(submissionId, res['JSESSIONID'], res['X-User-Sha1'], res['csrf_token'])
        flag = resp['result']
    except Exception as e:
        pass
    if flag:
        break
print(resp)

flag = False
resq = None
for i in range(0, 10):
    try:
        resq = getMessage(submissionId, res['JSESSIONID'], res['X-User-Sha1'])
        flag = resq['result']
    except Exception as e:
        pass
    if flag:
        break
print(resq)
