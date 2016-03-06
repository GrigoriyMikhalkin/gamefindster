from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^logout/$', views.logout),
    url(r'^profile/$', views.redirect_home)
]
