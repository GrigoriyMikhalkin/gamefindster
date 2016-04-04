from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^user/(?P<id>\d+)$', views.user_page),
    url(r'^group/(?P<id>\d+)$', views.group_page),
    url(r'^messages/$', views.messages),
    url(r'^events/(?P<gid>\d+)$', views.events),
    url(r'^notifications/$', views.notifications),
    url(r'^contacts/$', views.contacts),
    url(r'^contacts_g/$', views.contacts_g),
    url(r'^application/event/(?P<eid>\d+)$', views.request_event),
    url(r'^application/friend/(?P<uid>\d+)$', views.request_friend),
    url(r'^application/group/(?P<gid>\d+)$', views.request_group),
    url(r'^notification/accept/(?P<rid>\d+)$', views.accept),
    url(r'^notification/reject/(?P<rid>\d+)$', views.reject),
    url(r'^notification/delete/(?P<nid>\d+)$', views.delete_notification),
    url(r'^messages/(?P<uid>\d+)$', views.read_messages),
    url(r'^event/cancel/(?P<eid>\d+)$', views.cancel_event),
    url(r'^group/cancel/(?P<gid>\d+)$', views.cancel_group),
    url(r'^event/invite/(?P<uid>\d+)$', views.invite_event),
    url(r'^group/invite/(?P<uid>\d+)$', views.invite_group),
    url(r'^broadcast/event/(?P<eid>\d+)$', views.broadcast_event),
    url(r'^broadcast/group/(?P<gid>\d+)$', views.broadcast_group),
    url(r'^broadcast/friends/$', views.broadcast_friends),
]
