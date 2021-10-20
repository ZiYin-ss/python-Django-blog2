from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

#  自己写的用户登录的判断  原生的 但我们用的是Django内置的
def user_login(request):
    if request.method == "POST":
        login_from = LoginForm(request.POST)  # 有一个csrf的key value 会自己扔掉
        if login_from.is_valid():
            cd = login_from.cleaned_data
            #  这个地方是检验此用户是否为本网站项目的用户 以及其密码是否正确  如果都对上了就返回user实例对象
            #  注意自己这个账户 必须通过admin添加过呢
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                #  这个时候就登录成功 默认保存在session中了
                login(request, user)
                return HttpResponse("你已成功通过身份验证 登录成功 欢迎您")
            else:
                return HttpResponse("对不起 你的用户名或密码不正确")
        else:
            return HttpResponse("登录无效")
    if request.method == "GET":
        # 这个东西 你实例化 出来的就是html页面的 input框 用户名和密码的input框
        # 上面用这个数据 其实就是你在input输入了两个东西 就把那东西传递进去了 进行验证了
        login_form = LoginForm()
        return render(request,"account/login.html",{"form":login_form})
