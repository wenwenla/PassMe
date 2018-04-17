"""passme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import Score.views as av
import Pu.views as pv
import Ticks.views as tv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('score/', av.login_page),
    path('score/do_login/', av.do_login),
    path('score/info/', av.show_info),
    path('pu/', pv.login_page),
    path('pu/do_login/', pv.do_login),
    path('pu/info/', pv.info),
    path('ticks/', tv.index),
    path('ticks/login/', tv.login),
    path('ticks/logout/', tv.logout),
    path('ticks/wakeup/', tv.wakeup),
    path('ticks/sleep/', tv.sleep),
    path('ticks/other/', tv.other),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
