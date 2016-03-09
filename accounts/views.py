from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import UserPic

def is_owner(user,pic):
    return  user == pic.user

@login_required(login_url="/accounts/login/")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url="/accounts/login/")
def pic_delete(request,pid):
    pic = get_object_or_404(UserPic,id=pid)
    if is_owner(request.user,pic):
        if request.user.info.currentpic == pic:
            pic.delete()
            try:
                new_current = UserPic.objects.filter(user=request.user)[0]
                request.user.info.currentpic = new_current
            except IndexError:
                request.user.info.currentpic = None
            finally:
                request.user.info.save()
        else:
            pic.delete()
        
    return HttpResponseRedirect('/social/user/%d' % request.user.id)


@login_required(login_url="/accounts/login/")
def pic_change(request,pid):
    pic = get_object_or_404(UserPic,id=pid)
    if is_owner(request.user,pic):
        request.user.info.currentpic = pic
        request.user.info.save()
        
    return HttpResponseRedirect('/social/user/%d' % request.user.id)


def redirect_home(request):
    return HttpResponseRedirect("/")

