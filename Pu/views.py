from django.http import HttpResponseRedirect
from django.shortcuts import render
from Pu.pu import Pu, DataAnalysis
# Create your views here.


def login_page(request):
    return render(request, 'pu/login.html')


def do_login(request):
    name = request.POST.get('zh')
    password = request.POST.get('mm')
    if not name or not password:
        return HttpResponseRedirect('/pu/')
    p = Pu()
    if not p.login(name + '@hhu.com', password):
        return HttpResponseRedirect('/pu/')
    request.session['info'] = p.info
    return HttpResponseRedirect('/pu/info/')


def info(request):
    if not request.session.get('info'):
        return HttpResponseRedirect('/pu/')
    p = Pu(request.session['info'])
    if not p.is_login():
        return HttpResponseRedirect('/pu/')
    res = p.run()
    front_end_data = DataAnalysis(res).run()
    return render(request, 'pu/info.html', {'item': front_end_data})
