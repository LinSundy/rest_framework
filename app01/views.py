from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions


class MyAuthentication(object):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return ('alex', None)

    def authenticate_header(self, val):
        pass


class DogView(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request, *args, **kwargs):
        return HttpResponse('获取狗!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('更新狗')
