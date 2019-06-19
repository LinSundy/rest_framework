from django.urls import path,re_path
from . import views


urlpatterns = [
    re_path('^dog/', views.DogView.as_view())
]