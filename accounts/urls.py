from django.conf.urls import url
from django.contrib import admin
from .forms import mActivationView
from django.views.generic.base import TemplateView
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.hmac.views import RegistrationView

from . import views

urlpatterns = [
    url(r'^activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'
        ),
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>[-:\w]+)/$',
        mActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/$',
        RegistrationView.as_view(
            form_class = RegistrationFormUniqueEmail
        ),
        name='registration_register'),
    url(r'^picture/change/(?P<pid>\d+)$', views.pic_change),
    url(r'^picture/delete/(?P<pid>\d+)$', views.pic_delete),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^profile/$', views.redirect_home),
    url(r'^settings/(?P<uid>\d+)$', views.user_settings),
]
