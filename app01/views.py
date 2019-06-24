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
    ret = {
        'code': '0000',
        'msg': '请求成功',
        'token': ''
    }

    def post(self, request, *args, **kwargs):
        user = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        try:
            user_obj = UserInfo.objects.get(username=user)
            print(id(self.ret), 'id地址')
            if pwd == user_obj.password:
                token = md5(user)
                UserToken.objects.update_or_create(defaults={'userName': user, 'token': token})
                self.ret['token'] = token
                self.ret['msg'] = '请求成功'
            else:
                self.ret['msg'] = '用户名密码不正确'
                self.ret['token'] = ''
            return JsonResponse(self.ret)
        except UserInfo.DoesNotExist:
            self.ret['code'] = '4000'
            self.ret['msg'] = '当前用户名不存在！'
            self.ret['token'] = ''
            return JsonResponse(self.ret)
