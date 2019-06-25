from django.http import JsonResponse
from .models import UserInfo, UserToken
import datetime
import hashlib

# Create your views here.
from rest_framework.views import APIView


def md5(s):
    m1 = hashlib.md5()
    m1.update(bytes(s, encoding='utf-8'))
    current_time = datetime.datetime.now()
    m1.update(bytes(str(current_time), encoding='utf-8'))
    return m1.hexdigest()


class Login(APIView):

    def post(self, request, *args, **kwargs):
        ret = {
            'code': '0000',
            'msg': None,
        }
        user = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        try:
            user_obj = UserInfo.objects.get(username=user)
            if pwd == user_obj.password:
                token = md5(user)
                UserToken.objects.update_or_create(user=user_obj, defaults={'token': token})
                ret['token'] = token
                ret['msg'] = '请求成功'
            else:
                ret['code'] = '4000'
                ret['msg'] = '用户名密码不正确'
            return JsonResponse(ret)
        except UserInfo.DoesNotExist:
            ret['code'] = '4000'
            ret['msg'] = '当前用户名不存在！'
            return JsonResponse(ret)
