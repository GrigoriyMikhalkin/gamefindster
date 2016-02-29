from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^user/(?P<id>\d+)$', views.user_page),
    url(r'^messages/$', views.messages),
    url(r'^events/$', views.events),
    url(r'^notifications/$', views.notifications),
    url(r'^contacts/$', views.contacts),
    url(r'^application/(?P<eid>\d+)$', views.application),
    url(r'^notification/accept/(?P<aid>\d+)$', views.accept),
    url(r'^notification/reject/(?P<aid>\d+)$', views.reject),
    url(r'^notification/delete/(?P<nid>\d+)$', views.delete_notification),
    url(r'^notification/friend/(?P<uid>\d+)$', views.friend_request),
    url(r'^message/send/(?P<nid>\d+)$', views.send_message),
]
