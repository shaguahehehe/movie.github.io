from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse


def index(request):
    return render(request, "index.html")


# # 登录的校验
# def login(request):
#     verify_code = request.POST.get('captcha',None)
#     username = request.POST.get('username',None)
#     password = request.POST.get('password',None)
#     print(username)
#     print(password)
#     if verify_code == request.session['verifycode']:
#         if(~(username == None)):
#             try:
#                 stu = stu1.get(name=username)
#                 if username==stu.name and  stu.pwd==password:
#                     request.session['username']=username
#                     return redirect(reverse('select_sc',args=[1]))
#                 else:
#                     message={
#                         "context":'账号或密码错误'
#                     }
#                     return render(request,"login.html",message)
#             except :
#                 message = {
#                     "context": '账号或密码错误'
#                 }
#                 return render(request, "login.html", message)
#     else:
#         message = {
#             "context": '验证码错误'
#         }
#         return render(request,"login.html",message)


    # 画出验证码
  # 验证码
def verifycode(request):
    # 引入绘画模板
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量,用于画面的背景色,宽,高
    bg_color = (random.randrange(20, 100), random.randrange(20, 100), 255)
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
    request.session['verifycode'] = rand_str
    print(request.session['verifycode'])
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中,文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端,MIME类型为图片png
    return HttpResponse(buf.getvalue(), content_type='image/png')





