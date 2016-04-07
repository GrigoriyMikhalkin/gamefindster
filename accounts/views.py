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
from django.utils.translation import to_locale, get_language

# Import geo-stuff
from ipware.ip import get_real_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

# Import models
from .models import UserPic, UserPlatform
from base.models import Platform
from accounts.models import LanguageToUser
from django.contrib.auth.models import User
from cities.models import City, Country
from languages_plus.models import Language

SEX_TYPES = {
    "undefined": None,
    "male": True,
    "female": False,
}

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
    locale = to_locale(get_language())

    if user != request.user:
        return HttpResponseRedirect('/')

    # Birthdate setting
    birthdate = request.POST.get("birthdate")
    if birthdate:
        user.info.birthdate = birthdate
        user.info.save()
    
    # Sex setting
    sex = request.POST.get("sex")
    if sex:
        user.info.sex = SEX_TYPES[sex]
        user.info.save()

    # Languages setting
    selected_languages = request.POST.getlist("chk_languages[]")
    for language in selected_languages:
        ltu = LanguageToUser.objects.get_or_create(user=user,language=language)
    
    languages = Language.objects.all()
    user_languages = [ language.language for language in user.languages.all() ]

    # Platforms setting
    selected_platforms = request.POST.getlist("chk_platforms[]")
    for platform in selected_platforms:
        platform = Platform.objects.get(name=platform)
        up = UserPlatform.objects.get_or_create(user=user,platform=platform)
        
    platforms = Platform.objects.all()
    user_platforms = [ platform.platform.name for platform in user.platforms.all() ]
    
    
    # Location settings
    m_city = user.info.city
    if m_city == None:
        user_ip = get_real_ip(request)
        g = GeoIP2()
        location_info = g.city(user_ip)
        m_city = location_info["city"]
        m_country = location_info["country_name"]

        longitude = location_info["longitude"]
        latitude = location_info["latitude"]
        pnt = Point(longitude,latitude)

        try:
            m_city = City.objects.get(country__name=m_country,name=m_city,location__distance_lt=(pnt,D(km=10)))
        except City.DoesNotExist:
            location_info = g.city("213.208.167.83")
            m_city = location_info["city"]
            m_country = location_info["country_name"]

            longitude = location_info["longitude"]
            latitude = location_info["latitude"]
            pnt = Point(longitude,latitude)
            m_city = City.objects.get(country__name=m_country,name=m_city,location__distance_lt=(pnt,D(km=10)))      
        
        user.info.city = m_city
        user.info.save()

    if request.POST.get("latitude"):
        lat = float(request.POST.get("latitude"))
        lng = float(request.POST.get("longitude"))
        pnt = Point(lng,lat)

        m_city = City.objects.get(location__distance_lt=(pnt,D(km=2)))
        user.info.city = m_city
        user.info.save()

    m_country = m_city.country.name
    longitude = m_city.location.x
    latitude = m_city.location.y
      
    tz = request.POST.get('timezone')
    if tz:
        user.info.timezone = tz
        user.info.save()
        request.session['django_timezone'] = tz
        return HttpResponseRedirect('/accounts/settings/%s' % uid)
    
    context = {
        "timezones": pytz.common_timezones,
        "m_country": m_country,
        "m_city": m_city,
        "longitude": longitude,
        "latitude": latitude,
        "platforms": platforms,
        "user_platforms": user_platforms,
        "languages": languages,
        "user_languages": user_languages,
        "locale": locale,
    }
    
    return render(request, "accounts/settings_general.html", context)


def redirect_home(request):
    return HttpResponseRedirect("/")

