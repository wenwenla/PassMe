from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from Application.score import *
# Create your views here.


def login_page(request):
    session_id = Score.get_id()
    request.session['JSESSIONID'] = session_id
    score = Score(session_id)
    img_url = score.get_image()
    return render(request, 'login.html', {'img_url': img_url})


def do_login(request):
    name = request.POST.get('zjh')
    password = request.POST.get('mm')
    v_yzm = request.POST.get('v_yzm')
    if not name or not password or not v_yzm:
        return HttpResponseRedirect('/score/')
    session_id = request.session.get('JSESSIONID')
    if not session_id:
        return HttpResponseRedirect('/score/')
    score = Score(session_id)
    if not score.login(name, password, v_yzm):
        return HttpResponseRedirect('/score/')
    return HttpResponseRedirect('/info/')


def show_info(request):
    session_id = request.session.get('JSESSIONID')
    if not session_id:
        return HttpResponseRedirect('/score/')
    score = Score(session_id)
    info = score.phrase_page(score.get_score_page())
    result = score.get_result(info)
    return render(request, 'info.html', {'result': result, 'info': info})
