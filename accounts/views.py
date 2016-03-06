from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def redirect_home(request):
    return HttpResponseRedirect("/")
