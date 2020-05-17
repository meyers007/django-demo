from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.http import HttpResponseRedirect

import sys
sys.path.append("notebooks")
import ViewsCommon
from . import views

app_name = 'demo'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'', views.index, name='index'),
    path(r'demo/', views.index, name='index'),
    url(r'^.*/$', ViewsCommon.Common, name='catchall'),
]

