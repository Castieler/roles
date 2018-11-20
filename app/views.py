from django.shortcuts import render, redirect

from app.service.forms import LoginForm, RegistForm,SetPasswordForm
from rbac import models
from rbac.service.init_permission import init_permission
from django.contrib import messages
from functools import wraps

def validate(fun):
    def inner(request, *args, **kwargs):
        if request.session['username']:
            return fun(request, *args, **kwargs)
        else:
            return redirect('/login')
    return inner

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            print(username)
            password = form.cleaned_data['password']
            user_queryset = models.User.objects.filter(username=username).values('password_hash')
            print(password)
            password_hash = user_queryset[0].get('password_hash', '')
            if models.User().verify_password(password_hash, password):
                _user_queryset = models.User.objects.filter(username=username)
                request.session['username'] = str(_user_queryset[0])
                init_permission(_user_queryset[0], request)
                return redirect('/home/')
            else:
                return render(request, 'login.html',{"info": "密码错误"})
        else:
            return render(request, 'login.html', {"form": form})

@validate
def home(request):
    return render(request, 'home.html')


def regist(request):
    if request.method == 'GET':
        form = RegistForm()
        return render(request, 'regist.html', {"form": form})
    elif request.method == 'POST':
        form = RegistForm(data=request.POST)
        print('sss')
        if form.is_valid():
            username = form.cleaned_data['username']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = form.cleaned_data['password']
            print(username)
            print(password)
            user_queryset = models.User.objects.filter(username=username)
            if user_queryset:
                return render(request, "regist.html", {"errors": {'username':['此用户名已存在，请更换']}})
            else:
                models.User.objects.create(username=username,password=password)
                a = models.User.objects.get(username=username)
                xuesheng = models.Role.objects.get(id=4)
                a.roles.add(xuesheng)
                return render(request, "login.html", {"info": '注册成功'})

        else:
            print(form.errors)
            return render(request, "regist.html", {"errors": form.errors})


def set_password(request):
    if request.method == 'GET':
        form = SetPasswordForm()
        return render(request, 'set_pwd.html')
    elif request.method == 'POST':
        form = SetPasswordForm(data=request.POST)
        if form.is_valid():
            username = request.session['username']
            password = form.cleaned_data['password']
            models.User.objects.filter(username=username).update(password=password)
            return render(request, 'set_pwd.html', {"info": "已修改，请牢记密码"})

        else:
            return render(request, 'set_pwd.html')

def out(request):
    if request.method == 'GET':
        del request.session["username"]
        request.session.clear()
    return redirect('/login/')