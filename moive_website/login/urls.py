from django.contrib import admin
from django.urls import path, re_path
from  .  import  views
urlpatterns = [
    path("",views.index),
    re_path(r'yzm/[0-9]*', views.verifycode, name='yzm'),
]