from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login  # 1从 Django 默认的（或者说是内置的）用户认证和管理应用中引入的两个方法。
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from .models import UserProfile, UserInfo
from .forms import LoginForm, RegistrationForm
from .forms import UserProfileForm, UserInfoForm, UserForm
from QuestionApp.models import *


# Create your views here.
def user_login(request):  # 2视图函数中要处理前端提交的数据，井支持前端的显示请求
    if request.method == "POST":  # 3返回 HTTP请求类型的字符串
        login_form = LoginForm(request.POST)  # 4前端浏览器向服务器端提交表单内容
        if login_form.is_valid():  # 5验证所传入的数据是否合法
            cd = login_form.cleaned_data  # 6cd引用的是一个字典类型数据，其中以键值对的形式记录了用户名和密码。
            user = authenticate(username=cd['username'], password=cd['password'])
            # 7authenticate（）函数，其作用是检验此用户是否为本网站项目的用户,以及其密码是否正确.如果都对上号，就返回User的一个实例对象，否则返回None
            if user:
                login(request, user)  # 8login（）函数，以语句⑦所得到的User实例对象作为参数，实现用户登录
                return HttpResponse("Wellcom You. You have been authenticated successfully")  # 9
            else:
                return HttpResponse("Sorry. Your username or password is not right.")
        else:
            return HttpResponse("Invalid login")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse('question:index', args=[1]))
        else:
            return HttpResponseRedirect(reverse('account:user_register'))
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})


@login_required(login_url='/account/login/')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "question/my_center.html", {"user": user, "userinfo": userinfo, "userprofile": userprofile})


@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd["email"])
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return render(request, 'question/my_center.html')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})
        userinfo_form = UserInfoForm(
            initial={"school": userinfo.school, "company": userinfo.company, "profession": userinfo.profession,
                     "address": userinfo.address, "aboutme": userinfo.aboutme})
        return render(request, "account/myself_edit.html",
                      {"user_form": user_form, "userprofile_form": userprofile_form, "userinfo_form": userinfo_form})


# 改为可由前端传入图片
@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']  # 得到前端以POST方式提交的图片信息
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html', )


@login_required(login_url='/account/login/')
def my_collect(request):
    user = User.objects.get(id=request.user.id)
    collect_answers = user.collect_answer.all()
    collect_questions = user.collect_question.all()
    context = {"collect_answers": collect_answers, "collect_questions": collect_questions, }
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    context['userprofile'] = userprofile
    context['userinfo'] = userinfo
    return render(request, 'account/collections.html', context=context)
