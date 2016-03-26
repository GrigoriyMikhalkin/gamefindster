import pytz
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import deprecate_current_app
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from .models import UserPic
from django.contrib.auth.models import User

def is_owner(user,pic):
    return  user == pic.user

def _get_login_redirect_url(request, redirect_to):
    # Ensure the user-originating redirection URL is safe.
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        return resolve_url(settings.LOGIN_REDIRECT_URL)
    return redirect_to

@deprecate_current_app
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=auth.REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None, redirect_authenticated_user=False):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if redirect_authenticated_user and request.user.is_authenticated():
        redirect_to = _get_login_redirect_url(request, redirect_to)
        if redirect_to == request.path:
            raise ValueError(
                "Redirection loop for authenticated user detected. Check that "
                "your LOGIN_REDIRECT_URL doesn't point to a login page."
            )
        return HttpResponseRedirect(redirect_to)
    elif request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            tz = user.info.timezone
            request.session['django_timezone'] = tz
            return HttpResponseRedirect(_get_login_redirect_url(request, redirect_to))
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


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


@login_required(login_url="/accounts/login/")
def user_settings(request,uid):
    user = get_object_or_404(User,id=uid)
    if user == request.user:
        tz = request.POST.get('timezone')
        if tz:
            user.info.timezone = tz
            user.info.save()
            request.session['django_timezone'] = tz

        context = {
            "timezones": pytz.common_timezones,
        }    
        return render(request, "accounts/settings.html", context)
            
    return HttpResponseRedirect('/')


def redirect_home(request):
    return HttpResponseRedirect("/")
