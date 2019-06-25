from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^login/$', views.Login.as_view()),
    re_path('^register/$', views.Register.as_view())
]
