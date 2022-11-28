from django.http import JsonResponse

from sendEmail.views.student.yiban import yiban


JSESSIONID = "87C7B97342E00C348CED5F623A23A669"
num = "1668144593710"


def getInfo(request):
    data = request.POST
    user_id = data.get('user_id')
    global JSESSIONID, num
    # yb = yiban("21140", "180710", JSESSIONID, num)
    yb = yiban("22084", "25094X", JSESSIONID, num)

    res = None
    for i in range(3):
        res = yb.get_stu_info(user_id)
        if res == "unlogin":
            yb.signUp()
            JSESSIONID = yb.JSESSIONID
            num = yb.num
        else:
            break
    if res is None or res == "unlogin":
        return JsonResponse({
            'result': "false",
        })
    return JsonResponse({
        'result': "true",
        'user_id': res['user_id'],
        'school': res['school'],
        'nick': res['nick']
    }, json_dumps_params={'ensure_ascii': False})
