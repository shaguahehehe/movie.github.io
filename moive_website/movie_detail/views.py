import json
import os
import random
from datetime import datetime
from io import BytesIO

import qrcode
import xlwt
from django.core import serializers
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
import hashlib
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from pyecharts.globals import ThemeType

from  .Usercf import Usercf
from django.utils.cache import get_cache_key
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import HttpResponse, Http404, JsonResponse, HttpRequest
from  .itemcf import  itemcf
# Create your views here.
from django.views.decorators.cache import cache_page


def index(request):
    return render(request, "index.html")


# 查询电影
# @cache_page(30)
def select_moive(request):
    if request.method == "GET":
        movies_detail = MovieMessage.objects.all()
        movies_detail1 = MovieMessage.objects.all().order_by("-score")
        movie_list = str_dict(movies_detail)
        movie_list1 = str_dict(movies_detail1)
        movie_list['socre']=movie_list1
        return JsonResponse(movie_list)


# //把所有数据存储在列表
def str_dict(args):
    movie_dict = {}
    dianyi = []
    lianxj = []
    zongyi = []
    dongm = []
    for i in args:
        context = {}
        context["id"] = i.id
        context["title"] = i.title
        context["img"] = i.img
        context["score"] = i.score
        context["year"] = i.year
        context["star"] = i.star
        context["moive_id"] = i.moive_id
        if i.moive_id == 1:
            dianyi.append(context)
        if i.moive_id == 2:
            lianxj.append(context)
        if i.moive_id == 3:
            zongyi.append(context)
        if i.moive_id == 4:
            dongm.append(context)
    movie_dict["diany"] = dianyi
    movie_dict["lianxj"] = lianxj
    movie_dict["zongyi"] = zongyi
    movie_dict["dongm"] = dongm
    return movie_dict


def select_page(request, currpage=1):
    if request.method == "GET":
        movies_detail = MovieMessage.objects.all()
        paginator = Paginator(movies_detail, 8)
        if currpage <= 1:
            currpage = 1
        elif currpage >= paginator.num_pages:
            currpage = paginator.num_pages
        movies_detail = paginator.page(currpage)
        movie_list = str_dict(movies_detail)
        return JsonResponse(movie_list, safe=False)


def select_contain(request, currpage=1):
    if request.method == "GET":
        title = request.GET.get("title", "")
        info = request.GET.get("info", "")
        area = request.GET.get("area", "")
        type = request.GET.get("type", "")
        star = request.GET.get("star", "")
        alias = request.GET.get("alias", "")
        director = request.GET.get("director", "")
        language = request.GET.get("language", "")
        contains_data = MovieMessage.objects.filter(type__contains=type, title__contains=title, info__contains=info,
                                                    area__contains=area, star__contains=star, alias__contains=alias,
                                                    director__contains=director, language__contains=language)
        paginator = Paginator(contains_data, 8)
        if currpage <= 1:
            currpage = 1
        elif currpage >= paginator.num_pages:
            currpage = paginator.num_pages
        movies_detail = paginator.page(currpage)
        movie_list = str_dict(movies_detail)
        return JsonResponse(movie_list, safe=False)

    # 画出验证码


# 验证码
def captcha(request):
    # 引入绘画模板
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量,用于画面的背景色,宽,高
    bg_color = (random.randrange(20, 100), random.randrange(20, 100), 0)
    bg_width = 100
    bg_height = 25
    # 创建画面对象
    im = Image.new('RGB', (bg_width, bg_height), bg_color)
    # 创建笔画对象
    draw = ImageDraw.Draw(im)
    # 调用笔画的point()函数绘画噪点
    for i in range(0, 100):
        draw_xy = (random.randrange(0, bg_width), random.randrange(0, bg_height))
        draw_fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(draw_xy, fill=draw_fill)
    # 定义验证码的备选值
    candidate_str = 'ASDFGHJKLQWERTYUIO1234567890ZXCVBNM0987654321poiuytrewqlkjhgfdsamnbvcxz'
    # 随机选取四个字符作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += candidate_str[random.randrange(0, len(candidate_str))]
    # 构造字体对象
    font_obj = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMLI.TTF", 23)

    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制出随机选取的四个字符
    draw.text((5, 0), rand_str[0], font=font_obj, fill=fontcolor)
    draw.text((25, 0), rand_str[1], font=font_obj, fill=fontcolor)
    draw.text((50, 0), rand_str[2], font=font_obj, fill=fontcolor)
    draw.text((75, 0), rand_str[3], font=font_obj, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session, 用于做进一步验证
    request.session['captcha'] = rand_str
    print(request.session['captcha'])
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中,文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端,MIME类型为图片png
    return HttpResponse(buf.getvalue(), content_type='image/png')


# 登录验证
@csrf_exempt
def login(request):
    logininfo = request.body
    logininfo = json.loads(logininfo)
    username = logininfo['username']
    password = logininfo['password']
    captcha = logininfo['captcha']
    if captcha == request.session['captcha']:
        if (~(username == None)):
            try:
                stu1 = Stupwd.objects
                stu = stu1.get(name=username)
                pwd = hashlib.md5()
                pwd.update(password.encode())
                if username == stu.name and stu.pwd == pwd.hexdigest():
                    request.session['username'] = username
                    request.session['id'] = stu.id
                    result = {
                        "code": '200 ',
                        "msg": "登录成功",
                         "username":username
                    }
                    return JsonResponse(result)
                else:
                    result = {
                        "code": '206 ',
                        "msg": "账号或密码错误"
                    }
                    return JsonResponse(result)
            except:
                result = {
                    "code": '206 ',
                    "msg": "账号或密码错误"
                }
                return JsonResponse(result)
    else:
        result = {
            "code": '205 ',
            "msg": '验证码错误'
        }
        return JsonResponse(result)


def select_fenlei(request, moive_id):
    result = {
        "moive_id": moive_id
    }
    return render(request, "xianqi.html", result)


def select_moiveid(request):
    moive_id = request.GET.get("moive_id", "")
    currpage = request.GET.get("currpage", "")
    # type: type,
    # area: area,
    # year: year,
    # lanuage: lanuage,
    type = request.GET.get("type", "")
    lanuage=request.GET.get("lanuage","")
    area = request.GET.get("area", "")
    year = request.GET.get("year", "")
    if type=='全部':
        type=''
    if lanuage == '全部':
        lanuage = ''
    if area == '全部':
        area = ''
    if year == '全部':
        year = ''
    if currpage == "":
        currpage = 1
    else:
        currpage = int(currpage)
    if moive_id != "":
        moives_list = MovieMessage.objects.filter(moive_id=moive_id,type__contains=type
        ,language__contains=lanuage,area__contains=area,year__contains=year).all().order_by("score")
        paginator = Paginator(moives_list, 12)
        if currpage <= 1:
            currpage = 1
        elif currpage >= paginator.num_pages:
            currpage = paginator.num_pages
        movies_detail = paginator.page(currpage)
        moives = str_dict1(movies_detail, currpage)
        print(moives)
        # moives=serializers.serialize("json",movies_detail,fields=("id","title","info","img","area","type","star","alias","director","score","language","year"),ensure_ascii=False)
    return JsonResponse(moives, safe=False)


def str_dict1(args, currpage):
    movie_list = []
    for i in args:
        context = {}
        context["currpage"] = currpage
        context["id"] = i.id
        context["title"] = i.title
        context["info"] = i.info
        context["img"] = i.img
        context["area"] = i.area
        context["type"] = i.type
        context["star"] = i.star
        context["alias"] = i.alias
        context["director"] = i.director
        context["score"] = i.score
        context["language"] = i.language
        context["year"] = i.year
        context["moive_id"] = i.moive_id
        movie_list.append(context)
    return movie_list


def tologin(request):
    return render(request, "login.html")


def login_houtai(request):
    captcha = request.POST.get('captcha', None)
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print(username)
    print(password)
    if captcha == request.session['captcha']:
        if (~(username == None)):
            try:
                stu1 = Manager.objects
                stu = stu1.get(name=username)
            except:
                message = {
                    "context": '账号或密码错误'
                }
                return render(request, "login.html", message)
            pwd = hashlib.md5()
            pwd.update(password.encode())
            print(pwd.hexdigest())
            print(stu.name)
            if username == stu.name and stu.pwd == pwd.hexdigest():
                    print("ooo")
                    request.session['manager'] = username
                    print("ppp")
                    return redirect(reverse('houtaishouye', args=[1]))
            else:
                    message = {
                        "context": '账号或密码错误'
                    }
                    return render(request, "login.html", message)

    else:
        message = {
            "context": '验证码错误'
        }
        return render(request, "login.html", message)

def houtai_shouye(request, currpage=1):

    moviemesage = MovieMessage.objects.all()
    paginator = Paginator(moviemesage, 10)
    if currpage <= 1:
        currpage = 1
    elif currpage >= paginator.num_pages:
        currpage = paginator.num_pages
    clist = paginator.page(currpage)
    context = {
        "clist": clist,
        "currpage": currpage
    }
    return render(request, "houtai.html", context)





def to_excel(request):
    # 设置HTTPPResponse类型
    response = HttpResponse(content_type='application/ms-excel')
    # 设置文件名
    response['Content-Disposition'] = 'attachment; filename=result.xls'
    # 创建工作薄
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet("电影信息", cell_overwrite_ok=True)
    for i in range(1, 7):
        first_col = sheet.col(i)
        first_col.width = 256 * 15
    # font_style =xlwt.XFStyle()
    # font_style.font.bold = True
    # 初始化样式
    style_font = xlwt.XFStyle()
    style_alignment = xlwt.XFStyle()
    style_borders = xlwt.XFStyle()
    # 写入表格
    clist = []
    kebiao = ["电  影  名 字", "	电  影  信  息", "图  片  路  径", "电  影  地  区", "电  影  年  份", "电  影  语  言", "电  影  主 演",
              "电  影  别  名","电 影 类 型","电  影 分 类","电  影 分 数"]
    for row in range(len(kebiao)):
        sheet.write(0, row, kebiao[row])
    moives= MovieMessage.objects.all()
    han = 1
    # num=0
    for moive in moives:
        if moive.moive_id == 1:
            moivefenlei="电影"
        elif moive.moive_id == 2:
                moivefenlei = "连续剧"
        elif moive.moive_id == 3:
            moivefenlei = "综艺"
        elif moive.moive_id == 4:
            moivefenlei = "动漫"
        clist = [moive.title, moive.info, moive.img, moive.area,
                 moive.year,
                 moive.language, moive.star,moive.alias,moive.type, moivefenlei,moive.score]
        for lie, cr in enumerate(clist):
            sheet.write(han, lie, cr)
        han += 1
    # num+=1
    # if num== 8 :
    #     break
    font_style = xlwt.XFStyle()
    wb.save(response)
    return response
def to_data(request):
    return render(request,"todata.html")

def uploadfile(request):
    txt=request.FILES.get('txt',None)
    if txt ==None:
        return HttpResponse("上传失败")
    wenjw=txt.name.split(".")
    if wenjw[1] != "txt":
        return HttpResponse("请选择txt文件")
    file=open("D:\\upload\\"+wenjw[0]+"."+wenjw[1],"wb+")
    for chunk in txt.chunks():
        file.write(chunk)
    file.close()
    data_list=[]
    with open("D:\\upload\\"+wenjw[0]+"."+wenjw[1],"r",encoding="utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip()
            xinx = line.split('\t')
            print(xinx)
            print(len(xinx))
            # title, moive.info, moive.img, moive.area,
            # moive.year,
            # moive.language, moive.star, moive.alias, moive.type, moivefenlei, moive.score
            coolection_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            if xinx[9] == "电影":
                feilei=1
            elif xinx[9] == "连续剧":
                feilei=2
            elif xinx[9] == "综艺":
                    feilei = 3
            elif xinx[9] == "综艺" :
                    feilei = 4
            else:
                return HttpResponse("内容格式不对")
            moive = MovieMessage(title=xinx[0],info=xinx[1],img=xinx[2],area=xinx[3],
                                  year=xinx[4],language=xinx[5],star=xinx[6],alias=xinx[7],type=xinx[8],moive_id=feilei,score=xinx[10],addtime=coolection_time,updatetime=coolection_time)

            data_list.append(moive)
    MovieMessage.objects.bulk_create(data_list)
    return HttpResponse("上传成功")

def  grmessage(request):
    stu=Manager.objects.filter(name=request.session['manager'])[0]
    context={
        "stu":stu
    }
    return render(request,"grmessage.html",context)


def sous(request,currpage=1):
    clist=[]
    sous=request.GET.get('sous',None)
    print(sous)
    if sous==None or sous=='':
        return redirect(reverse('houtaishouye',args=[1]))
    try:
        moives=MovieMessage.objects.filter(title__contains=sous)
        print(moives)
        # for moive in moives:
        #     clist.append(moive)
        paginator = Paginator(moives, 5)
        if currpage < 1:
            currpage = 1
        elif currpage > paginator.num_pages:
            currpage = paginator.num_pages
        clist = paginator.page(currpage)
    except:
        HttpResponse("请重新输入搜索条件，区分大小写")
    context = {
            "clist": clist,
           "currpage":currpage
        }
    return render(request, "houtai.html", context)
def updateuser(request,id):
    pass
# 删除电影
def delectdiany(request,id):
    print("进入")
    print(id)
    movie=MovieMessage.objects.filter(id=id)
    movie.delete()
    return redirect(reverse('houtaishouye', args=[1]))
# 读取对于的课程
def updatediany(request,id):
    moive = MovieMessage.objects.filter(id=id)[0]
    context={
        "moive":moive
    }
    return render(request,"update.html",context)
def updatemiove(request):
        try:
            movie = MovieMessage.objects
            movie = movie.get(id=request.POST['id'])
            movie.title = request.POST['title']
            movie.info = request.POST['info']
            movie.area = request.POST['area']
            movie.type = request.POST['type']
            movie.star = request.POST['star']
            movie.alias = request.POST['alias']
            movie.year = request.POST['year']
            movie.language = request.POST['language']
            print(request.POST['moive_id'])
            if request.POST['moive_id'] == '电影':
                movie.moive_id = 1
            elif request.POST['moive_id'] == '连续剧':
                movie.moive_id = 2
            elif request.POST['moive_id'] == '综艺':
                movie.moive_id = 3
            elif request.POST['moive_id'] == '动漫':
                movie.moive_id = 4
            else:
                movie.moive_id = 5
            movie.save()
        except Exception as e:
            print(e)
            return HttpResponse("修改失败,请正确填写")
        else:
            return redirect(reverse('houtaishouye', args=[1]))


def insertdiany(request):
    return render(request,"insertmoive.html")


def insert(request):
    title = request.POST.get('title', None)
    info = request.POST.get('info', None)
    area = request.POST.get('area', None)
    type = request.POST.get('type', None)
    star = request.POST.get('star', None)
    alias = request.POST.get('alias', None)
    year = request.POST.get('year', None)
    language = request.POST.get('language', None)
    img = request.POST.get('img', None)
    director = request.POST.get('director', None)
    score = request.POST.get('score', None)
    moive_id = request.POST.get('moive_id', None)
    if moive_id == '电影':
        moive_id = 1
    elif moive_id == '连续剧':
        moive_id = 2
    elif moive_id == '综艺':
        moive_id = 3
    elif moive_id == '动漫':
        moive_id = 4
    else:
        moive_id = 5
    # try:

    MovieMessage.objects.create(title=title, info=info, area=area, type=type, star=star,
                                      alias=alias,year=year,language=language,moive_id=moive_id,img=img,director=director,score=score)
    return redirect(reverse('houtaishouye', args=[1]))


def leix(request):
    pass


def selectmoiveid(request):
    id=request.GET.get("id",None)
    context={
        "id":id
    }
    return render(request,"moivemessage.html",context)


def selectmoiveidmessage(request):
    id=request.GET.get("id",None)
    userid=request.session.get("id", "")

    qr = qrcode.QRCode()  # 事实上里面的参数我们可以都不指定，默认会选择一个比较合适的参数
        # 调用add_data，指定url。
    qr.add_data("https://www.baidu.com/")
    # "http://127.0.0.1:9000/selectmoiveid/?id=" + id
    # 生成二维码图像
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(r"D:\moive-website\moive_website\static\erwma\baidu.png")
                # 保存到硬盘上
    # if os.path.exists(r"D:\moive-website\moive_website/static/erwma/" + str(id) + ".png"):
    #     pass
    # else:
    #     img.save(r"D:\moive-website\moive_website/static/erwma/" + str(id) + ".png")
    # # 事实上，这个img实际上是通过PIL模块得到的，可以理解为里面Image对象
    # # 如果你熟悉PIL模块的话，那么你应该知道可以将里面Image对象保存成图片对应的字节流
    # buf = BytesIO()
    # img.save(buf)  # 将字节保存到buf里面
    # with open("../static/erwma/"+str(id)+".png", "wb") as f:
    #     f.write(buf.getvalue())  # 和直接保存为1.png是一样的
    tjmoives = []
    itemtjmoives=[]
    if  userid !="":
        # 根据用户相似度推荐
        if UserEvaluation.objects.filter(user_id=userid).count() ==0:
            shul=MovieMessage.objects.all().count()
            moive_message=MovieMessage.objects.filter().values('id','type',"title")
            while True:
                suijmoive = moive_message[random.randint(0, shul-1)]
                tjmoives.append(suijmoive)
                if len(tjmoives) == 5:
                    break
        else:
            user_info = UserEvaluation.objects.all()
            data = readdata(user_info)
            usercf = Usercf(data)
            tjdiany = usercf.recommend(userid)
            if tjdiany !=[]:
                for  tj in tjdiany:
                        tjmoive=MovieMessage.objects.filter(id=int(tj[0])).values('id','type',"title")[0]
                        tjmoives.append(tjmoive)
            else:
                shul = MovieMessage.objects.all().count()
                moive_message = MovieMessage.objects.filter().values('id', 'type', "title")
                while True:
                    suijmoive = moive_message[random.randint(0, shul - 1)]
                    tjmoives.append(suijmoive)
                    if len(tjmoives) == 5:
                        break
        # 根据物品相似度推荐
        if UserEvaluation.objects.filter(movie_id=id).count() ==0:
            shulitem = MovieMessage.objects.all().count()
            moive_message=MovieMessage.objects.filter().values('id','star',"title","img")
            while True:
                suijmoive = moive_message[random.randint(0, shulitem-1)]

                itemtjmoives.append(suijmoive)
                if len(itemtjmoives) == 10:
                    break
        else:
            user_info = UserEvaluation.objects.all()
            item_dict = readdata_item(user_info)
            itemcfsous = itemcf(item_dict)
            itemxianshilist=itemcfsous.top_simliar(id)
            for  itemtj in itemxianshilist:
                    tjmoive=MovieMessage.objects.filter(id=int(itemtj[0])).values('id',"title",'star',"img")[0]
                    itemtjmoives.append(tjmoive)
        # ok=serializers.serialize("json",tjmoive,ensure_ascii=False)
    moive=MovieMessage.objects.filter(id=id).values('id','type','area','year','language','star',
    "director","alias","img","info","title","score")

    moive=list(moive)
    suijmoivelist = MovieMessage.objects.filter().values('id',"title",'star',"img")
    if tjmoives !=[] or itemtjmoives !=[]:
        if len(tjmoives) >= 5:
            tjmoives = tjmoives[:5]
        else:
             while True:
                suijmoive=suijmoivelist[random.randint(0,suijmoivelist.count()-1)]
                tjmoives.append(suijmoive)
                if len(tjmoives) == 5:
                     break
        if  len(itemtjmoives) >= 10:
            itemtjmoives = itemtjmoives[:10]
        else:
            while True:
                suijmoive = suijmoivelist[random.randint(0, suijmoivelist.count()-1)]
                itemtjmoives.append(suijmoive)
                if len(itemtjmoives) == 10:
                    break
        context={
            "onemoive":moive,
             "tjmoives":tjmoives,
            "itemtjmoives":itemtjmoives
        }
    else:
        context = {
            "onemoive": moive
        }
    return JsonResponse(context)
def readdata(datas):
    guanx={}
    for data in datas:
        if not data.user_id in guanx.keys():
              guanx[data.user_id]={data.movie_id:data.score}
        else:
            guanx[data.user_id][data.movie_id]=data.score
    return guanx
def readdata_item(datas):
    itemguanx={}
    for data in datas:
         if  not data.movie_id in itemguanx.keys():
            itemguanx[data.movie_id]={data.user_id:data.score}
         else:
            itemguanx[data.movie_id][data.user_id]=data.score
    return itemguanx
@csrf_exempt
def xinzengpingf(request):
    pingfinfo=request.body
    pingfinfo = json.loads(pingfinfo)
    id=pingfinfo['id']
    score=pingfinfo['score']
    userid=request.session.get("id","")
    if userid == "":
        result={
            "code":205,
            "msg":"你还没有登录，不能推荐"
        }
        return JsonResponse(result)
    else:
        print(userid)
        try:
            UserEvaluation.objects.create(user_id=userid,movie_id=id,score=score)
        except Exception as e:
            print(e)
            result = {
                "code": 205,
                "msg": "评分错误,你可能评分过了"
            }
            return JsonResponse(result)
        else:
            result={
                "code": 200,
                "msg": "评分成功，谢谢的对这部电影的评分"
            }
            return JsonResponse(result)


def logout(request):
    request.session["username"]=""
    result={
        "code":200,
        "message":"登录成功"
    }
    return JsonResponse(result)


def sousmoivemessage(request):
    sous=request.GET.get("sous","")
    context={
        "sous":sous
    }
    # }
    return render(request,"moivesousye.html",context)


def sousmoive(request,currpage=1):
    currpage = request.GET.get("currpage", 1)
    souscontent=request.GET.get("souscontent","")
    sousmoive=MovieMessage.objects.filter(title__contains=souscontent).values('id','type','area','year','language','star',
    "director","alias","img","info","title","score").order_by("id")
    # sousmoive = list(sousmoive)
    print(type(sousmoive))
    paginator=Paginator(sousmoive,5)
    if int(currpage) <= 1:
        currpage = 1
    elif int(currpage) >= paginator.num_pages:
        currpage = paginator.num_pages
    sousmoive=paginator.page(currpage)
    sousmoive=list(sousmoive)
    result={
        "sousmoive":sousmoive,
         "currpage":currpage
    }
    return JsonResponse(result,safe=False)


def playermoive(request):
    id=request.GET.get("id","")

    qr = qrcode.QRCode()  # 事实上里面的参数我们可以都不指定，默认会选择一个比较合适的参数
        # 调用add_data，指定url。
    # qr.add_data("http://127.0.0.1:9000/selectmoiveid/?id=" + str(id))
    qr.add_data("https://www.baidu.com/")
        # "http://127.0.0.1:9000/selectmoiveid/?id=" + id
        # 生成二维码图像
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(r"D:\moive-website\moive_website\static\erwma\baidu.png")
    # if os.path.exists(r"D:\moive-website\moive_website/static/erwma/" + str(id) + ".png"):
    #   pass
    # else:
    #     img.save(r"D:\moive-website\moive_website/static/erwma/" + str(id) + ".png")
    result={
    "id":id
    }
    return render(request,"player.html",result)


def playermoivemessage(request):
    itemtjmoives = []
    id=request.GET.get("moiveid","")
    userid = request.session.get("id", "")
    if userid !="":
        if UserEvaluation.objects.filter(movie_id=id).count() == 0:
            shulitem = MovieMessage.objects.all().count()
            moive_message = MovieMessage.objects.filter().values('id', 'type', "title",'star', "img")
            while True:
                suijmoive = moive_message[random.randint(0, shulitem - 1)]
                itemtjmoives.append(suijmoive)
                if len(itemtjmoives) == 10:
                    break
        else:
            user_info = UserEvaluation.objects.all()
            item_dict = readdata_item(user_info)
            itemcfsous = itemcf(item_dict)
            itemxianshilist = itemcfsous.top_simliar(id)
            for itemtj in itemxianshilist:
                tjmoive = MovieMessage.objects.filter(id=int(itemtj[0])).values('id', "title", 'star', "img")[0]
                itemtjmoives.append(tjmoive)
    moivemsg = MovieMessage.objects.filter(id=id).values('id', 'type', 'area', 'title', 'year', 'info')
    moivemsg = list(moivemsg)
    suijmoivelist = MovieMessage.objects.all()
    if itemtjmoives != []:
            if  len(itemtjmoives) >= 10:
                itemtjmoives = itemtjmoives[:10]
            else:
                while True:
                    suijmoive = suijmoivelist[random.randint(0, suijmoivelist.count()-1)]
                    itemtjmoives.append(suijmoive)
                    if len(itemtjmoives) == 10:
                        break
            content = {
                "moivemsg": moivemsg,
                "itemtjmoives": itemtjmoives
            }
    else:
        content = {
            "moivemsg": moivemsg
        }
    return JsonResponse(content)


def tuichu(request):
    request.session["manager"]=""
    return render(request,"login.html")


def moivecount(request):
    score = ['0-1分', '1-2分', '2-3分', '3-4分', '4-5分', '5-6分', '6-7分', ">7分"]
    moiveppingfdict={}
    pingfcount = []
    moivemsg=MovieMessage.objects.all()
    for moive in  moivemsg:
        if moive.score!="" or moive.score!=None:
            if int(float(moive.score)) >=0 and int(float(moive.score)) <1:
                if_moiveppingfdict('0-1分',moiveppingfdict)
            elif int(float(moive.score)) >=1 and int(float(moive.score)) < 2:
                if_moiveppingfdict('1-2分', moiveppingfdict)
            elif int(float(moive.score)) >=2 and int(float(moive.score)) < 3:
                if_moiveppingfdict('2-3分', moiveppingfdict)
            elif int(float(moive.score)) >= 3 and int(float(moive.score)) < 4:
                if_moiveppingfdict('3-4分', moiveppingfdict)
            elif int(float(moive.score)) >= 4 and int(float(moive.score)) < 5:
                if_moiveppingfdict('4-5分', moiveppingfdict)
            elif int(float(moive.score)) >= 5 and int(float(moive.score)) < 6:
                if_moiveppingfdict('5-6分', moiveppingfdict)
            elif int(float(moive.score)) >= 6 and int(float(moive.score)) < 7:
                if_moiveppingfdict('6-7分', moiveppingfdict)
            elif int(float(moive.score)) >= 7 :
                if_moiveppingfdict('>7分', moiveppingfdict)
    for value in moiveppingfdict.values():
                    pingfcount.append(value)
    c = (
        Bar(init_opts=opts.InitOpts(width="600px",
                                    height="350px",
                                    page_title="电影分数统计",
                                    theme=ThemeType.DARK))
            .add_xaxis(score)
            .add_yaxis("电影评分统计分布", pingfcount)
            .set_global_opts(title_opts=opts.TitleOpts(title="电影统计"))
    )
    return HttpResponse(c.render_embed())
def if_moiveppingfdict(str,moiveppingfdict):
    if str in moiveppingfdict.keys():
        moiveppingfdict[str] += 1
    else:
        moiveppingfdict[str] = 0
def if_containtype(str,moivetypedict):
    if str in moivetypedict.keys():
        moivetypedict[str] += 1
    else:
        moivetypedict[str] = 0

def pingf(request):
    type = ["剧情", "动作", "惊悚", "犯罪", "奇幻", "冒险", "悬疑", "科幻", "伦理", "喜剧"]
    moivetypedict = {}
    typecount = []
    moivetypes = MovieMessage.objects.all()
    for moivetype in moivetypes:
        if "剧情" in moivetype.type:
            if_containtype("剧情", moivetypedict)
        elif "动作" in moivetype.type:
            if_containtype("动作", moivetypedict)
        elif "惊悚" in moivetype.type:
            if_containtype("惊悚", moivetypedict)
        elif "犯罪" in moivetype.type:
            if_containtype("犯罪", moivetypedict)
        elif "奇幻" in moivetype.type:
            if_containtype("奇幻", moivetypedict)
        elif "冒险" in moivetype.type:
            if_containtype("冒险", moivetypedict)
        elif "悬疑" in moivetype.type:
            if_containtype("悬疑", moivetypedict)
        elif "科幻" in moivetype.type:
            if_containtype("科幻", moivetypedict)
        elif "伦理" in moivetype.type:
            if_containtype("伦理", moivetypedict)
        elif "喜剧" in moivetype.type:
            if_containtype("喜剧", moivetypedict)
    print(moivetypedict)
    # ['0-1分', '1-2分', '2-3分', '3-4分', '4-5分', '5-6分', '6-7分', "<7分"]
    for value in moivetypedict.values():
        typecount.append(value)
    pie = (
        # 创建饼图
        Pie(init_opts=opts.InitOpts( width="800px",
                                    height="750px",page_title="电影类型统计",theme=ThemeType.DARK))

            # 为饼图增加标签和数据
            .add("", list(zip(type, typecount)))
            # 为饼图增加主标题和副标题
            .set_global_opts(title_opts=opts.TitleOpts(title="类型数量统计", subtitle="单位: (个)"))
            # 为饼图增加数据标签
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}\n({d}%)"))
            .set_global_opts(title_opts=opts.TitleOpts(title="电影统计"))
    )
    return HttpResponse(pie.render_embed())


def register(request):
    return render(request,"register.html")


def registeruser(request):
    account=request.POST.get("account")
    password = request.POST.get("password")
    try:
        user=Stupwd.objects.get(name=account)
        content={
            "content":"账号已注册"
        }
        return render(request,"register.html",content)
    except:
         md=hashlib.md5()
         md.update(password.encode())
         Stupwd.objects.create(name=account,pwd=md.hexdigest())
    return render(request,"index.html")


def updatemanager(request):
    return HttpResponse("ok")