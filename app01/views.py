from django.http import JsonResponse
from .models import UserInfo, UserToken
from rest_framework import exceptions
import datetime
import hashlib

# Create your views here.
from rest_framework.views import APIView

# 简单定义一下order的数据
orderData = {
    'code': '0000',
    'data': [
        {
            'yagao': {
                'price': 3,
            },
            'yashua': {
                'price': 2
            }
        }
    ]
}


def md5(s):
    m1 = hashlib.md5()
    m1.update(bytes(s, encoding='utf-8'))
    current_time = datetime.datetime.now()
    m1.update(bytes(str(current_time), encoding='utf-8'))
    return m1.hexdigest()


class Auth(object):
    def authenticate(self, request):
        ret = {
            'code': '0000',
            'msg': None
        }
        token = request.data.get('token');
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败！')
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass


class Login(APIView):
    """
    用于用户登录
    """
    authentication_classes = []

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


class Register(APIView):
    """
    用户用户注册
    """

    def post(self, request, *args, **kwargs):
        ret = {
            'code': '0000',
            'msg': '请求成功'
        }
        username = request._request.POST.get('username')
        password = request._request.POST.get('password')
        userType = request._request.POST.get('userType')
        if not username or not password:
            ret['code'] = '4000'
            ret['msg'] = '缺少必要参数'
        else:
            user_type = userType or 1
            try:
                usernameObj = UserInfo.objects.get(username=username)
                ret['code'] = '4000'
                ret['msg'] = '用户名重复'
            except UserInfo.DoesNotExist:
                UserInfo.objects.create(username=username, password=password, user_type=user_type)

        return JsonResponse(ret)


class Order(APIView):
    # authentication_classes = [Auth, ]
    def get(self, request):
        return JsonResponse(orderData)
