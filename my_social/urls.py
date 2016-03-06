from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^user/(?P<id>\d+)$', views.user_page),
    url(r'^messages/$', views.messages),
    url(r'^events/$', views.events),
    url(r'^notifications/$', views.notifications),
    url(r'^contacts/$', views.contacts),
    url(r'^application/event/(?P<eid>\d+)$', views.request_event),
    url(r'^application/friend/(?P<uid>\d+)$', views.request_friend),
    url(r'^notification/accept/(?P<rid>\d+)$', views.accept),
    url(r'^notification/reject/(?P<rid>\d+)$', views.reject),
    url(r'^notification/delete/(?P<nid>\d+)$', views.delete_notification),
    url(r'^messages/(?P<uid>\d+)$', views.read_messages),
]
