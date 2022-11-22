from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # 首页
    path('', views.index, name="index"),
    # 首页的查询电影
    path('select_moive/', views.select_moive, name="select_moive"),
    # 分页查询
    path('select_page/', views.select_page, name="select_page"),

    path('select_contain/', views.select_contain, name="select_contain"),
    # 登录逻辑
    path('login/', views.login, name="login"),
    # 类型点击更多
    path('select_fenlei/<int:moive_id>', views.select_fenlei, name="select_fenlei"),
    # 验证码
    re_path(r'yzm/[0-9]*', views.captcha, name='yzm'),
    # 查询电影分页显示
    path(r'select_moiveid', views.select_moiveid, name="select_moiveid"),
    # 类型显示
    path(r'selectmoiveid/', views.selectmoiveid, name="selectmoiveid"),
    # 电影信息
    path(r'selectmoiveidmessage/', views.selectmoiveidmessage, name="selectmoiveidmessage"),
    # 电影评分
    path(r'xinzengpingf/', views.xinzengpingf, name="xinzengpingf"),

    path(r'logout/', views.logout, name="logout"),
path(r'register/', views.register, name="register"),
path(r'registeruser/', views.registeruser, name="registeruser"),

    path(r'sousmoivemessage/', views.sousmoivemessage, name="sousmoivemessage"),
    path(r'sousmoive/', views.sousmoive, name="sousmoive"),
    path(r'playermoive/', views.playermoive, name="playermoive"),
    path(r'playermoivemessage/', views.playermoivemessage, name="playermoivemessage"),

    path("houtai/", views.tologin, name="houtai"),
    path("login_houtai/", views.login_houtai, name="login_houtai"),
    path("houtai_shouye/<int:currpage>", views.houtai_shouye, name="houtaishouye"),
    path("tuichu/", views.tuichu, name="tuichu"),
    path("moivecount/", views.moivecount, name="moivecount"),

    path("sous/<int:currpage>", views.sous, name="sous"),
    path('updateuser/', views.updateuser, name='updateuser'),
    # 转成excel表
    path('toexcel/', views.to_excel, name='toexcel'),

    path('to_data/', views.to_data, name='todata'),

    path('pingf/', views.pingf, name='pingf'),

    path('uploadfile/', views.uploadfile, name='uploadfile'),

    # 查询并跳转个人信息
    path("grmessage/", views.grmessage, name="grmessage"),
    # 删除电影
    path('delectdiany/<int:id>', views.delectdiany, name='delectdiany'),
    # 修改电影
    path('updatediany/<int:id>', views.updatediany, name='updatediany'),
    path('updatemiove/', views.updatemiove, name='updatemiove'),
    path('insertdiany/', views.insertdiany, name='insertdiany'),
    path('insert/', views.insert, name='insert'),
    path('leix/', views.leix, name='leix'),

    path('updatemanager/', views.updatemanager, name='updatemanager')

]
