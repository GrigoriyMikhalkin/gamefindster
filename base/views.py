from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from .models import (Game, Event)
from .forms import EventForm
from my_social.models import Participation
from accounts.models import Language,LanguageToEvent, UserSearchSettings
from endless_pagination.decorators import page_template
from django.contrib.auth.decorators import login_required

from haystack.query import SearchQuerySet

# Create your views here.

@page_template("base/games_index_page.html")
def index(request,template="base/index.html",extra_context=None):
    """
    Shows scrollable list of most popular games
    """
    games = Game.objects.all()
    context = {
        "games": games,
        "request": request
    }
    if extra_context is not None:
        context.update(extra_context)
        
    return render(request,template,context)


def show_game_events(request,id):
    game = get_object_or_404(Game, id=id)
    event_list = game.event_set.filter(is_full=False,before__gt=timezone.now())

    if request.user.is_authenticated():
        user_search_settings = UserSearchSettings.objects.get(user=request.user)
        if user_search_settings.language:
            langs = [ lang for lang in request.user.search_languages.all() ]
            event_list = event_list.filter(languages__language__in=langs)

        if user_search_settings.time:
            pass

        if user_search_settings.location:
            pass
    
    paginator = Paginator(event_list,25)

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    form = EventForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.game = game
        instance.owner = request.user
        instance.save()
        
        participation = Participation(event=instance,participant=request.user,is_host=True)
        participation.save()

        languages = form.cleaned_data["languages"]
        if len(languages) == 0:
            instances = ( LanguageToEvent(event=instance,language=lang) for lang in request.user.languages.all() )
            LanguageToEvent.objects.bulk_create(instances)
        else:
            instances = (LanguageToEvent(event=instance,language=Language.objects.get(name=name)) for name in languages)
            LanguageToEvent.objects.bulk_create(instances)
        
        return HttpResponseRedirect("/game/%s" % id)
    
    context = {
        "game": game,
        "events": events,
        "request": request,
        "form": form
    }
    return render(request,"base/game_detail.html",context)


def show_event_details(request,id):
    event = get_object_or_404(Event, id=id)
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
