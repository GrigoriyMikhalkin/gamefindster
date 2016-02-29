from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^game/(?P<id>\d+)$', views.show_game_events),
    url(r'^event/(?P<id>\d+)$', views.show_event_details),
]
