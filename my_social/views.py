from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .Messaging.NotificationSender import *
from django.db.models import Q, F, Max
from django.contrib.auth.decorators import login_required
from gputils.functions import get_object_or_none
from endless_pagination.decorators import page_template

# Import models
from django.contrib.auth.models import User
from .models import *
from base.models import Event
from accounts.models import UserInfo


# Create your views here.
NOTIFICATION_TYPES = {
    "event_application": EventRequestSender,
    "friend_application": FriendRequestSender,
    "group_application": GroupRequestSender,
    "event_invitation": EventInviteSender,
    "group_invitation": GroupInviteSender,
}

def user_page(request,id):
    user = get_object_or_404(User,id=id)
    events = user.participation_set.all()
    city = user.info.city
    m_events = None
    m_groups = None

    if request.user.is_authenticated():
        m_events = request.user.event_set.filter(is_active=True)
        m_groups = request.user.group_set.all()

    try:
        country = city.country
        location = country.name + ", " + city.name
    except AttributeError:
        location = ""
    
    if request.user != user: 
        form = MessageForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.receiver = user
            instance.sender = request.user
            instance.save()
            
            return HttpResponseRedirect("/social/user/%s" % id)
    else:    
        form = UserPicForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            user.info.currentpic = instance
            user.info.save()
            return HttpResponseRedirect("/social/user/%s" % id)
    
    context = {
        "user": user,
        "events": events,
        "m_events": m_events,
        "m_groups": m_groups,
        "request": request,
        "form": form,
        "location": location,
    }
    return render(request, "my_social/userpage.html", context)

def group_page(request,id):
    group = get_object_or_404(Group,id=id)
    group_events = group.groupevent_set.all()

    if request.user.is_authenticated():
        participant = get_object_or_none(GroupParticipation,group=group,participant=request.user)
            
    else:
        participant = None
        
    if not participant: 
        form = MessageForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.receiver = group.owner
            instance.sender = request.user
            instance.save()
            return HttpResponseRedirect("/social/group/%s" % id)

    elif group.owner == request.user:    
        form = GroupPicForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.group = group
            instance.save()
            gcp = group.currentpic
            gcp.currentpic=instance
            gcp.save()
            return HttpResponseRedirect("/social/group/%s" % id)

    else:
        form = None

    # elif user is admin -- start event
    # elif user is participant -- apply to admin if admin application is open
        
    context = {
        "group": group,
        "group_events": group_events,
        "request": request,
        "form": form,
        "participant": participant,
    }
    return render(request, "my_social/grouppage.html", context)


def info_template(request,objects,pagination_size,section,template="my_social/info_template.html",form=None,extra_context=None):
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
        "section": section,
        "form": form,
    }
    if extra_context is not None:
        context.update(extra_context)
    
    return render(request,template,context)


@login_required(login_url="/accounts/login/")
@page_template("my_social/conversations_page.html")
def messages(request,template="my_social/infolist_template.html",extra_context=None):
    user = request.user
    conversations = user.received.order_by("sender","-created").distinct("sender")

    context = {
        "conversations": conversations,
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request,template,context)


@login_required(login_url="/accounts/login/")
@page_template("my_social/notifications_page.html")
def notifications(request,template="my_social/infolist_template.html",extra_context=None):
    user = request.user
    notifications = Notification.objects.filter(receiver=user)
    context = {
        "notifications": notifications,
    }
    if extra_context is not None:
        context.update(extra_context)
    
    return render(request,template,context)
    


@login_required(login_url="/accounts/login/")
@page_template("my_social/events_page.html")
def events(request, gid,template="my_social/infolist_template.html",extra_context=None):
    user = User.objects.get(id=gid)
    participations = Participation.objects.filter(participant=user).order_by("-event__start_time")
    current_date = datetime.now()
    
    context = {
        "participations": participations,
        "current_date": current_date,
    }
    if extra_context is not None:
        context.update(extra_context)
    
    return render(request,template,context)


@login_required(login_url="/accounts/login/")
def contacts(request):
    user = request.user
    
    objects = Friend.objects.filter(user_id=user.id)
    
    return info_template(request,objects=objects, pagination_size=50, section="contacts1", template="my_social/friends.html")

@login_required(login_url="/accounts/login/")
def contacts_g(request):
    user = request.user
    
    objects = GroupParticipation.objects.filter(participant=user)

    form = GroupForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.owner = user
        instance.save()
        GroupParticipation.objects.create(group=instance,participant=user,admin=True)
        GroupCurrentPic.objects.create(group=instance)
        return HttpResponseRedirect("/social/contacts_g/")
    
    return info_template(request,objects=objects, pagination_size=50, section="contacts2",\
                         form=form, template="my_social/groups.html")


def request_notification(user,receiver,request_object,request_sender):
    sender = request_sender(user,request_object)
    if sender.get_application_permission():
        sender.send_notification(receiver)
    else:
        return HttpResponse("<center><h1>You're not permitted to send this request</h1></center>")
    
    return HttpResponseRedirect('/')
    

def request_event(request,eid):
    user = request.user
    event = get_object_or_404(Event,id=eid)
    receiver = event.owner
    request_sender = EventRequestSender

    return request_notification(user,receiver,event,request_sender)


def request_friend(request,uid):
    user = request.user
    receiver = get_object_or_404(User,id=uid)
    request_sender = FriendRequestSender

    return request_notification(user,receiver,receiver,request_sender)


def request_group(request,gid):
    user = request.user
    group = get_object_or_404(Group,id=gid)
    receiver = group.owner
    request_sender = GroupRequestSender

    return request_notification(user,receiver,group,request_sender)


def accept(request,rid):
    user = request.user
    user_request = get_object_or_404(Request,id=rid)

    request_sender = NOTIFICATION_TYPES[user_request.notification.type]

    response_sender = request_sender.load_notification(user,user_request)

    if response_sender:
        response_sender.accept()
    
    return HttpResponseRedirect('/')


def reject(request,rid):
    user = request.user
    user_request = get_object_or_404(Request,id=rid)

    request_sender = NOTIFICATION_TYPES[user_request.notification.type]

    response_sender = request_sender.load_notification(user,user_request)

    if response_sender:
        response_sender.reject()
    
    return HttpResponseRedirect('/')


@login_required(login_url="/accounts/login/")
def delete_notification(request,nid):    
    notification = get_object_or_404(Notification,id=nid)
    user = request.user

    if request.user != notification.receiver:
        return HttpResponse("<center><h1>You are not receiver of this notification</h1></center>")
        
    notification.delete()
    return HttpResponseRedirect('/social/notifications/')

@login_required(login_url="/accounts/login/")
@page_template("my_social/messages_page.html")
def read_messages(request,uid,template="my_social/infolist_template.html",extra_context=None):
    user = request.user
    request_user = User.objects.get(id=uid)

    form = MessageForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receiver = request_user
        instance.sender = user
        instance.save()
        
        return HttpResponseRedirect("/social/messages/%s" % uid)
    
    
    messages = Message.objects.filter((Q(receiver=user) & Q(sender=request_user))
                                     | (Q(receiver=request_user) & Q(sender=user)))

    context = {
        "messages": messages,
        "form": form,
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request,template,context)


@login_required(login_url="/accounts/login/")
def broadcast_event(request,eid):
    event = get_object_or_404(Event,id=eid)
    text = request.POST.get("broadcast-text")

    broadcaster = EventBroadcaster(request.user,event)
    broadcaster.broadcast(text)

    return HttpResponseRedirect("/event/%s" % eid)

@login_required(login_url="/accounts/login/")
def broadcast_group(request,gid):
    group = get_object_or_404(Group,id=gid)
    text = request.POST.get("broadcast-text")
    
    broadcaster = GroupBroadcaster(request.user,group)
    broadcaster.broadcast(text)

    return HttpResponseRedirect("/social/group/%s" % gid)
    

@login_required(login_url="/accounts/login/")
def broadcast_friends(request):
    user = request.user
    text = request.POST.get("broadcast-text")
    friend_filter = request.POST.get("friend-filter") 
    
    broadcaster = FriendBroadcaster(request.user)
    broadcaster.broadcast(text,friend_filter)

    return HttpResponseRedirect("/social/user/%s" % user.id)

@login_required(login_url="/accounts/login/")
def cancel_event(request,eid):
    event = get_object_or_404(Event,id=eid)
    text = request.POST.get("cancel-text")
    if request.user == event.owner:
        broadcaster = CancellationBroadcaster(request.user)
        broadcaster.broadcast_event(event,text)
        event.delete()

    return HttpResponseRedirect("/")

@login_required(login_url="/accounts/login/")
def cancel_group(request,gid):
    group = get_object_or_404(Group,id=gid)
    text = request.POST.get("cancel-text")
    if request.user == group.owner:
        broadcaster = CancellationBroadcaster(request.user)
        broadcaster.broadcast_group(group,text)
        group.delete()

    return HttpResponseRedirect("/")

@login_required(login_url="/accounts/login/")
def invite_event(request,uid):
    receiver = get_object_or_404(User,id=uid)
    eid = request.POST.get("eventid")
    event = get_object_or_404(Event,id=eid)
    text = request.POST.get("invite-text")
    
    if request.user == event.owner:
        invite_sender = EventInviteSender(request.user,event)
        invite_sender.send_notification(receiver,text)

    return HttpResponseRedirect("/social/user/%s" % uid)

@login_required(login_url="/accounts/login/")
def invite_group(request,uid):
    receiver = get_object_or_404(User,id=uid)
    gid = request.POST.get("groupid")
    group = get_object_or_404(Group,id=gid)
    text = request.POST.get("invite-text")
    
    if request.user == group.owner:
        invite_sender = GroupInviteSender(request.user,group)
        invite_sender.send_notification(receiver,text)

    return HttpResponseRedirect("/social/user/%s" % uid)
