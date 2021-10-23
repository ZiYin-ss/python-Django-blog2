from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse


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
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    if request.method == "POST":
        userprofile_form = UserProfileForm(request.POST)
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            # 因为上面只插入这个表是不是只插入这俩个字段  所以说 要把这次插入得对应user表得那个对象给他 会自己取出来id得 记住就好了
            new_profile.save()
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return HttpResponse("对不起注册失败 不能注册")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})


@login_required()  # 判断用户是否登录 还可以传递参数 要是没登录 让他去登录 其实这个地方已经判断了
#  如果没登录 他会自己让你去登录 我们在setting里面配置的 login_url就是的了
def myself(request):
    #  request.user 这个user是admin 其实是一条数据 里面保存了 user的信息
    #  不要说这几行代码看不懂啊 就是 去另外两个表查找有关当前登录用户的信息 有就展示 没有就创建 没有插入数据 就是设置了user=xxx
    #  插入数据 还是一个对象 自己就可以拿回来用了
    userprofile = UserProfile.objects.get(user=request.user) if \
        hasattr(request.user, 'userprofile') else \
        UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if \
        hasattr(request.user, 'userinfo') else \
        UserInfo.objects.create(user=request.user)
    return render(request, "account/myself.html",
                  {"user": request.user, "userinfo": userinfo, "userprofile": userprofile})


@login_required(login_url='/account/login')  # 可以不写 写了也没啥 配置过了
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if \
        hasattr(request.user, 'userprofile') else \
        UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if \
        hasattr(request.user, 'userinfo') else \
        UserInfo.objects.create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:  # 这个地方的作用是把基本信息给出去 编辑不也是可以看的吗
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth,
                                                    "phone": userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school,
                                              "company": userinfo.company,
                                              "profession": userinfo.profession,
                                              "address": userinfo.address,
                                              "aboutme": userinfo.aboutme})
        return render(request, "account/myself_edit.html",
                      {"user_form": user_form,
                       "userprofile_form": userprofile_form,
                       "userinfo_form": userinfo_form})


@login_required(login_url='/account/login')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)  # 先把原来的数据取出来 然后 多添加一个字段
        userinfo.photo = img
        userinfo.save()  # 再保存
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html', )
