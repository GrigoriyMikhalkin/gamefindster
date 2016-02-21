from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^user/(?P<id>\d+)$', views.user_page),
]
