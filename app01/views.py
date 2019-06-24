from django.http import JsonResponse
from .models import UserInfo, UserToken

# Create your views here.
from rest_framework.views import APIView


class Login(APIView):
    ret = {
        'code': '0000',
        'msg': '请求成功'
    }

    def post(self, request, *args, **kwargs):
        user = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        print(type(self.ret))
        try:
            user_obj = UserInfo.objects.get(username=user)
            print(type(user_obj))
            print(user_obj.password, '哇喔')
            return JsonResponse(self.ret)
        except UserInfo.DoesNotExist:
            self.ret['code'] = '4000'
            self.ret['msg'] = '当前用户名不存在！'
            return JsonResponse(self.ret)
