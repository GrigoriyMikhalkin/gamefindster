from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Message, Notification, Friend, Participation, Application
from base.models import Event
import time

# Create your views here.

def user_page(request,id):
    user = get_object_or_404(User,id=id)
    events = user.participation_set.all()

    context = {
        "user": user,
        "events": events,
        "request": request
    }
    return render(request, "social/userpage.html", context)

def info_template(request,objects,pagination_size,section):
    """
    For use in 'messages', 'events' and 'contacts'
    """
    paginator = Paginator(objects,pagination_size)

    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {
        "request": request,
        "objects": objects,
        "section": section
    }
    return render(request,"social/info_template.html",context)

def messages(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=404)
    
    objects = Message.objects.filter(receiver=user)
    
    return info_template(request,objects=objects, pagination_size=20, section="messages")

def notifications(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=404)
    
    objects = Notification.objects.filter(receiver=user)
    
    return info_template(request,objects=objects, pagination_size=20, section="notifications")
    
def events(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=404)
    
    objects = Participation.objects.filter(participant=user)
    
    return info_template(request,objects=objects, pagination_size=20, section="events")

def contacts(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=404)
    
    objects = Friend.objects.filter(user_id=user.id)
    
    return info_template(request,objects=objects, pagination_size=50, section="contacts")

def application(request, eid):
    user = request.user
    event = get_object_or_404(Event,id=eid)

    """
    Check that
    1) User is authenticated
    2) Not already participant of the event
    3) There is still free places
    """
    if (not user.is_authenticated()):
        return HttpResponse("<center><h1>You are not logged in</h1></center>")
    
    already_participant = event.participation_set.filter(participant=user).exists()
    if already_participant:
        return HttpResponse("<center><h1>You already participate in this event</h1></center>")

    if event.is_full:
        return HttpResponse("<center><h1>This event is already full</h1></center>")
    
    receiver = event.participation_set.get(event=event,is_host=True).participant
    text = ""
    notification = Notification(receiver=receiver,type="application",text=text)
    notification.save()
    
    application = Application(notification=notification,event=event,applicant=request.user)
    application.save()
    
    return HttpResponseRedirect('/')

def accept(request,aid):
    application = get_object_or_404(Application,id=aid)
    applicant = application.applicant
    event = application.event
    user = request.user
    """
    Check that
    1) User is authenticated
    2) User is host of event
    3) There free space in event
    4) Event is still active
    """
    if (not user.is_authenticated()):
        return HttpResponse("<center><h1>You are not logged in</h1></center>")

    if event.participation_set.filter(participant=user).exists():
        is_host = event.participation_set.get(participant=user).is_host
    else:
        is_host = False

    if (not is_host):
        return HttpResponse("<center><h1>You are not host of this event</h1></center>")

    if event.is_full:
        return HttpResponse("<center><h1>This event is already full</h1></center>")

    participation = Participation(event=event,participant=application.applicant)
    participation.save()

    # Delete activated notification
    application.notification.delete()

    # Send notification that applicant is accepted
    text = "You're accepted to participate in event '%s'" % event.name
    notification = Notification(receiver=applicant,type="acceptance",text=text)
    notification.save()
    
    application = Application(notification=notification,event=event,applicant=applicant)
    application.save()

    if event.participation_set.all().count() == event.participant_number:
        event.is_full=True
        event.save()
    

    return HttpResponseRedirect('/')
    
def reject(request,aid):
    application = get_object_or_404(Application,id=aid)
    applicant = application.applicant
    event = application.event
    user = request.user
    """
    Check that
    1) User is authenticated
    2) User is host of event
    """
    if (not user.is_authenticated()):
        return HttpResponse("<center><h1>You are not logged in</h1></center>")

    if event.participation_set.filter(participant=user).exists():
        is_host = event.participation_set.get(participant=user).is_host
    else:
        is_host = False

    if (not is_host):
        return HttpResponse("<center><h1>You are not host of this event</h1></center>")

    # Delete activated notification
    application.notification.delete()

    # Send notification that applicant is accepted
    text = "You're refused to participate in event '%s'" % event.name
    notification = Notification(receiver=applicant,type="acceptance",text=text)
    notification.save()
    
    application = Application(notification=notification,event=event,applicant=applicant)
    application.save()
    return HttpResponseRedirect('/')


def delete_notification(request,nid):    
    notification = get_object_or_404(Notification,id=nid)
    user = request.user
    if (not user.is_authenticated):
        return HttpResponse("<center><h1>You are not logged in</h1></center>")

    if request.user != notification.receiver:
        return HttpResponse("<center><h1>You are not receiver of this notification</h1></center>")
        
    notification.delete()
    return HttpResponseRedirect('/social/notifications/')

def friend_request(request,uid):
    pass

def send_message(request):
    pass
