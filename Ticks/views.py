import random

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone

from Ticks.forms import *
from Ticks.models import *
# Create your views here.


@login_required(login_url='/ticks/login/')
def index(request):
    user = request.user.profile
    my_event = Event.objects.filter(user=user).order_by('-date', '-time')
    p_event = Event.objects.filter(user=user.partner).order_by('-date', '-time')

    qs = my_event | p_event
    data = []
    for i in qs[:30]:
        data.append({
            'name': i.user.user.username,
            'date': i.date,
            'time': i.time,
            'title': i.title,
            'content': i.content,
            'self': i.user == user,
        })
    return render(request, 'ticks/time_line.html', {'data': data, 'username': user.user.username})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'ticks/login.html', {'form': form, 'password_is_wrong': True})
        user = auth.authenticate(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
        if not user or not user.is_active:
            return render(request, 'ticks/login.html', {'form': form, 'password_is_wrong': True})
        auth.login(request, user)
        return HttpResponseRedirect('/ticks/')
    else:
        form = LoginForm()
        return render(request, 'ticks/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/ticks/login/')


@login_required(login_url='/ticks/login/')
def wakeup(request):
    choice = ['起床啦~', '爬起来了~', '好困啊，起来了！']
    ret = {'status': 'ok', 'message': 'success'}
    user = request.user.profile

    now = timezone.now()
    if Event.objects.filter(class_type='W', date=now.date(), user=user).exists():
        ret['status'] = 'error'
        ret['message'] = '不要重复起床打卡啊，乖~'
        return JsonResponse(ret)
    try:
        Event.objects.create(user=user, class_type='W', title=random.choice(choice), content=request.POST['content'])
    except:
        ret['status'] = 'error'
        ret['message'] = '你想黑了我的服务器啊！'

    return JsonResponse(ret)


@login_required(login_url='/ticks/login/')
def sleep(request):
    choice = ['睡觉啦~', '开始躺尸~', '困死了，睡觉了！']
    ret = {'status': 'ok', 'message': 'success'}
    user = request.user.profile

    now = timezone.now()
    if Event.objects.filter(class_type='S', date=now.date(), user=user).exists():
        ret['status'] = 'error'
        ret['message'] = '一天睡两次是想干啥啊~'
        return JsonResponse(ret)
    try:
        Event.objects.create(user=user, class_type='S', title=random.choice(choice), content=request.POST['content'])
    except:
        ret['status'] = 'error'
        ret['message'] = '你想黑了我的服务器啊！'

    return JsonResponse(ret)


@login_required(login_url='/ticks/login/')
def other(request):
    ret = {'status': 'ok', 'message': 'success'}
    user = request.user.profile

    content = request.POST['content']

    if ':' in content:
        title = content.split(':')[0]
        content = content.split(':')[1]
    else:
        title = '随手记录'

    try:
        Event.objects.create(user=user, class_type='O', title=title, content=content)
    except:
        ret['status'] = 'error'
        ret['message'] = '你想黑了我的服务器啊！'

    return JsonResponse(ret)
