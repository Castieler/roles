"""version3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views
from django.views import static
from . import settings
from django.conf.urls import handler404, handler500
# handler404 = "app.views.page_not_found"
# handler500 = "app.views.page_error"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^home/', views.home),
    url(r'^regist/', views.regist),
    url(r'^set_pwd/', views.set_password),
    url(r'^out/', views.out),
    url(r'^list_index/', views.list_index),
    url(r'^list_type/(\w+)/', views.list_type),
    url(r'^list_field/(\w+)/(\w+)/', views.list_field),
    url(r'^create_table/', views.create_table),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
]
