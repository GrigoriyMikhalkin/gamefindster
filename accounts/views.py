from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def login(request):
    context = {}
    return render(request,"accounts/login.html",context)

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect("/accounts/register_success")

    context = {
        "form": UserCreationForm()
    }
    return render(request,"accounts/register.html",context)

def register_success(request):
    context = {}
    return render(request,"accounts/register_success.html",context)
