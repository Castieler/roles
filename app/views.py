import requests
import json
import traceback
from django.shortcuts import render, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.service.forms import LoginForm, RegistForm, SetPasswordForm
from rbac import models
from rbac.service.init_permission import init_permission
from conf import es_conf
from django.views.decorators.cache import cache_page  # 导入设置缓存的装饰器


def validate(fun):
    def inner(request, *args, **kwargs):
        if request.session['username']:
            return fun(request, *args, **kwargs)
        else:
            return redirect('/login')
    return inner


def save_request_url(fun):
    def inner(request, *args, **kwargs):
        try:
            last_url = request.session['url']
        except:
            last_url= "/home/"
        request.session['url'] = request.path_info
        return fun(request, last_url, *args, **kwargs)

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
                print('sss123')
                init_permission(_user_queryset[0], request)

                return redirect('/home/')
            else:
                return render(request, 'login.html', {"info": "密码错误"})
        else:
            return render(request, 'login.html', {"form": form})


@validate
@save_request_url
def home(request, last_url):
    return render(request, 'home.html')


def regist(request):
    if request.method == 'GET':
        form = RegistForm()
        return render(request, 'regist.html', {"form": form})
    elif request.method == 'POST':
        form = RegistForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = form.cleaned_data['password']
            user_queryset = models.User.objects.filter(username=username)
            if user_queryset:
                return render(request, "regist.html", {"errors": {'username': ['此用户名已存在，请更换']}})
            else:
                password_hash = str(generate_password_hash(password))
                models.User.objects.create(username=username, password_hash=password_hash)
                a = models.User.objects.get(username=username)
                xuesheng = models.Role.objects.get(id=1)
                a.roles.add(xuesheng)
                return render(request, "login.html", {"info": '注册成功'})

        else:
            print(form.errors)
            return render(request, "regist.html", {"errors": form.errors})

@cache_page(100)
@save_request_url
def set_password(request,last_url):
    if request.method == 'GET':
        form = SetPasswordForm()
        return render(request, 'set_pwd.html')
    elif request.method == 'POST':
        form = SetPasswordForm(data=request.POST)
        if form.is_valid():
            username = request.session['username']
            password = form.cleaned_data['password']
            password_hash = str(generate_password_hash(password))
            models.User.objects.filter(username=username).update(password_hash=password_hash)
            return render(request, 'set_pwd.html', {"info": "已修改，请牢记密码"})

        else:
            return render(request, 'set_pwd.html', {"errors": form.errors})


@save_request_url
def out(request,last_url):
    if request.method == 'GET':
        del request.session["username"]
        request.session.clear()
    return redirect('/login/')


@cache_page(20)
@save_request_url
def list_index(request, last_url):
    if request.method == 'GET':
        print('last_url', last_url)
        es_name = request.GET.get('es_name')
        print(es_name)
        if not es_name:
            es_url = request.session['es_url']
            if not es_url:
                return redirect("/home")
            else:
                es_name = es_url
        print(es_conf.ES_INDEX_URL.format(es_url=es_name))
        request.session['es_url'] = es_name
        try:
            response = requests.get(es_conf.ES_INDEX_URL.format(es_url=es_name),
                                    headers={'Content-Type': 'application/json'}, timeout=4)
            if response.status_code != 200:
                return render(request, 'home.html', {'info': '集群地址不存在，请重新输入！'})
        except:
            return render(request, 'home.html', {'info': '集群地址不存在，请重新输入！'})
        try:
            _es_index = []
            es_index = json.loads(response.text)
            for item in es_index:
                _dict = {}
                for k, v in item.items():
                    _dict[k.replace('.', '_')] = v
                _es_index.append(_dict)
            return render(request, 'es/list_index.html', {'es_index': _es_index, 'url': last_url, 'tablename': '索引列表'})
        except Exception as e:
            traceback.print_exc()
            return redirect("/home")
    return redirect("/home")


@cache_page(20)
@save_request_url
def list_type(request, last_url, es_index):
    if request.method == 'GET':
        print('last_url',last_url)
        es_url = request.session['es_url']
        response = requests.get(es_conf.ES_TYPE_URL.format(es_url=es_url), headers={'Content-Type': 'application/json'})
        try:
            _list = []
            es_type = json.loads(response.text)
            _es_type = es_type[es_index]['mappings']
            for k, v in _es_type.items():
                _list.append(k)
            print(request.path_info)
            return render(request, 'es/list_type.html',
                          {'es_type': _list, 'url': last_url, 'es_index': es_index, 'tablename': '类型列表'})
        except Exception as e:
            traceback.print_exc()
            return redirect("/home")
    return redirect("/home")


@cache_page(20)
@save_request_url
def list_field(request, last_url, es_index, es_type):
    if request.method == 'GET':
        es_url = request.session['es_url']
        response = requests.get(es_conf.ES_TYPE_URL.format(es_url=es_url), headers={'Content-Type': 'application/json'})
        try:
            _list = []
            data = json.loads(response.text)
            _es_type = data[es_index]['mappings'][es_type]['properties']
            for k, v in _es_type.items():
                if v.get('properties', ''):
                    continue
                _list.append({'field': k, 'type': v.get('type', '')})
            return render(request, 'es/list_field.html',
                          {'fields': _list, 'url': last_url, 'es_index': es_index, 'es_type': es_type, 'tablename': '字段列表'})
        except Exception as e:
            traceback.print_exc()
            return redirect("/home")
    return redirect("/home")


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lib.python_hive import cur
import traceback


@csrf_exempt
def create_table(request):
    if request.method == 'POST':

        postBody = request.body.decode()
        data = eval(postBody)
        table_name = data.get('table_name', '')
        field_list = data.get('data', '')
        index = data.get('index', '')
        type = data.get('type', '')
        if not table_name or not field_list or not index or not type:
            return JsonResponse({"result": 1, "msg": "缺少参数"})
        select_hql = 'show create table ' + table_name
        print('select_hql', select_hql)
        try:
            cur.execute(select_hql)
            res = cur.fetchall()
            print('---')
            return JsonResponse({"result": 2, "msg": "此表名已存在！！！"})
        except Exception as e:
            # traceback.print_exc()
            print(e)
        _field_str = ''
        for item in field_list:
            print(item)
            if _field_str:
                _field_str = _field_str + ',' + "`" + item['field'] + "`" + " " + 'string' + " COMMENT 'from deserializer'"
            else:
                _field_str = _field_str + '' + "`" + item['field'] + "`" + " " + 'string' + " COMMENT 'from deserializer'"

        try:
            hql = es_conf.HIVE_SQL_BASE.format(es_nodes=es_conf.ES_NODES, index=index, type=type, table_name=table_name,
                                               field_str=_field_str)
            print(hql)
            cur.execute(hql)
            return JsonResponse({"result": 0, "msg": "创建成功"})
        except Exception as e:
            # traceback.print_exc()
            print(e)
            return JsonResponse({"result": 2, "msg": "创建失败，请确认表名"})


from django.shortcuts import render_to_response


def page_not_found(request):
    return render_to_response('error/404.html')


def page_error(request):
    return render_to_response('error/500.html')
