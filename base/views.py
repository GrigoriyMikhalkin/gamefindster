from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from .forms import EventForm
from endless_pagination.decorators import page_template
from django.contrib.auth.decorators import login_required

# Import models
from .models import (Game, Event)
from my_social.models import Participation
from accounts.models import Language,LanguageToEvent,UserSearchSettings

# Import search
from haystack.query import SearchQuerySet

LOC_CODES = {
    "0": "CITY",
    "100": "REGION",
    "200": "COUNTRY",
    "300": "WORLD",
}

@page_template("base/games_index_page.html")
def index(request,template="base/index.html",extra_context=None):
    """
    Shows scrollable list of most popular games
    """
    if request.user.is_authenticated() and request.user.info.is_first_time():
        return HttpResponseRedirect("/accounts/settings/location/%s" % request.user.id)
    
    games = Game.objects.all()
    context = {
        "games": games,
        "request": request,
    }
    if extra_context is not None:
        context.update(extra_context)
        
    return render(request,template,context)


@page_template("base/events_page.html")
def show_game_events(request,id,template="base/game_detail.html",extra_context=None):
    user = request.user
    game = get_object_or_404(Game, id=id)
    event_list = game.event_set.filter(is_full=False,before__gt=timezone.now())
    form = None
    location_value = None
    
    if user.is_authenticated():

        user_search_settings = UserSearchSettings.objects.get(user=user)

        location_code = request.POST.get("location")
        if location_code:
            user.search_settings.location = location_code

        if request.POST.get("time-filter"):
            user_search_settings.time = True

            beginning = request.POST.get("period-start")
            ending = request.POST.get("period-end")

            beginning = datetime.strptime(beginning,"%Y-%m-%d %H:%M")
            ending = datetime.strptime(ending,"%Y-%m-%d %H:%M")

            if ending>beginning and ending>datetime.now():
                user_search_settings.beginning = beginning
                user_search_settings.ending = ending

        elif request.POST.get("period-off"):
            user_search_settings.time = False

        if request.POST.get("platform-filter"):
            user_search_settings.platform = True

            platforms = request.POST.getlist("chk_platforms[]")
            user_platforms = user.platforms.all()
            user_platforms.filter(platform__name__in=platforms).update(search=True)
            user_platforms.exclude(platform__name__in=platforms).update(search=False)
            
        elif request.POST.get("platform-off"):
            user_search_settings.platform = False
        
        if request.POST.get("lang-filter"):
            user_search_settings.language = True
            
            langs = request.POST.getlist("chk_languages[]")
            user_languages = user.languages.all()
            user_languages.filter(language__name__in=langs).update(search=True)
            user_languages.exclude(language__name__in=langs).update(search=False)

        elif request.POST.get("language-off"):
            user_search_settings.language=False

        # Save user's search settings
        user_search_settings.save()

        # Location range
        location_value = user.search_settings.location
        
        if LOC_CODES[location_value] != "WORLD":
            if LOC_CODES[location_value] == "CITY":
                event_list = event_list.filter(location=request.user.info.city)
            elif LOC_CODES[location_value] == "REGION":
                event_list = event_list.filter(location__region=request.user.info.city.region)
            elif LOC_CODES[location_value] == "COUNTRY":
                event_list = event_list.filter(location__country=request.user.info.city.country)

        if user_search_settings.time:
            beginning = user_search_settings.beginning
            ending = user_search_settings.ending
            event_list = event_list.filter(start_time__range=(beginning,ending))
                
        if user_search_settings.platform:
            platforms = [ platform.platform for platform in user.platforms.filter(search=True)]
            event_list = event_list.filter(platform__in=platforms)
            
        if user_search_settings.language:
            langs = [ lang.language for lang in user.languages.filter(search=True)]
            event_list = event_list.filter(languages__language__in=langs).distinct()

        form = EventForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.game = game
            instance.owner = user
            instance.location = user.info.city
            instance.save()
            
            participation = Participation(event=instance,participant=user,is_host=True)
            participation.save()

            languages = form.cleaned_data["languages"]
            if len(languages) == 0:
                instances = (LanguageToEvent(event=instance,language=lang.language) for lang in request.user.languages.all() )
                LanguageToEvent.objects.bulk_create(instances)
            else:
                instances = (LanguageToEvent(event=instance,language=Language.objects.get(name=name)) for name in languages)
                LanguageToEvent.objects.bulk_create(instances)
            
            return HttpResponseRedirect("/game/%s" % id)
    
    context = {
        "game": game,
        "events": event_list,
        "request": request,
        "form": form,
        "location_value": location_value,
    }
    if extra_context is not None:
        context.update(extra_context)
    
    return render(request,template,context)


def show_event_details(request,id):
    event = get_object_or_404(Event, id=id)
    participant = None
    
    if request.user.is_authenticated():
        participant = event.participation_set.filter(participant=request.user)

    context = {
        "event": event,
        "request": request,
        "participant": participant,
    }
    return render(request,"base/event_detail.html",context)


@page_template("base/games_index_page.html")
def game_search(request,template="base/index.html",extra_context=None):
    q = request.GET.get("q")

    games = Game.objects.filter(name__istartswith=q)
    context = {
        "request": request,
        "games": games,
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request,template,context)

@login_required(login_url="/accounts/login/")
def send_notification():
    pass
