from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^auth/$', views.auth_view),
    url(r'^register/$', views.register),
    url(r'^register_success/$', views.register_success),
]
