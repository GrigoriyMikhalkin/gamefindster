from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from .models import (Game, Event)
from .forms import EventForm
from social.models import Participation

# Create your views here.

def index(request):
    """
    Shows scrollable list of most popular games
    """
    games = Game.objects.all()
    context = {
        "games": games,
        "request": request
    }
    return render(request,"base/index.html",context)

def show_game_events(request,id):
    game = get_object_or_404(Game, id=id)
    event_list = game.event_set.filter(is_full=False)
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
        instance.save()
        participation = Participation(event=instance,participant=request.user,is_host=True)
        participation.save()
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
    context = {
        "event": event,
        "request": request
    }
    return render(request,"base/event_detail.html",context)
