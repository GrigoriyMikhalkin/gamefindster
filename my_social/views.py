from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import *
from .forms import MessageForm, UserPicForm
from base.models import Event
from .Messaging.NotificationSender import *
from django.db.models import Q, Max

# Create your views here.
NOTIFICATION_TYPES = {
    "event_application": EventRequestSender,
    "friend_application": FriendRequestSender 
}

def user_page(request,id):
    user = get_object_or_404(User,id=id)
    events = user.participation_set.all()
    
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
        "request": request,
        "form": form
    }
    return render(request, "my_social/userpage.html", context)

def info_template(request,objects,pagination_size,section,form=None):
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
    return render(request,"my_social/info_template.html",context)

def messages(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(status=404)
    
    objects = user.received.order_by("sender","-created").distinct("sender")
    
    return info_template(request,objects=objects, pagination_size=20, section="messages_l1")

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


def request_notification(user,receiver,request_object,request_sender):
    sender = request_sender(user,receiver,request_object)
    if sender.get_application_permission():
        sender.send_notification()
    else:
        return HttpResponse("<center><h1>You're not permitted to send this request</h1></center>")
    
    return HttpResponseRedirect('/')
    

def request_event(request,eid):
    user = request.user
    event = get_object_or_404(Event,id=eid)
    receiver = event.participation_set.get(event=event,is_host=True).participant
    request_sender = EventRequestSender

    return request_notification(user,receiver,event,request_sender)
    
def request_friend(request,uid):
    user = request.user
    receiver = get_object_or_404(User,id=uid)
    request_sender = FriendRequestSender

    return request_notification(user,receiver,receiver,request_sender)
    

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


def delete_notification(request,nid):    
    notification = get_object_or_404(Notification,id=nid)
    user = request.user
    if (not user.is_authenticated):
        return HttpResponse("<center><h1>You are not logged in</h1></center>")

    if request.user != notification.receiver:
        return HttpResponse("<center><h1>You are not receiver of this notification</h1></center>")
        
    notification.delete()
    return HttpResponseRedirect('/social/notifications/')

def read_messages(request,uid):
    user = request.user
    request_user = User.objects.get(id=uid)
    if not user.is_authenticated():
        return HttpResponse(status=404)

    form = MessageForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receiver = request_user
        instance.sender = user
        instance.save()
        return HttpResponseRedirect("/social/messages/%s" % uid)
    
    
    objects = Message.objects.filter((Q(receiver=user) & Q(sender=request_user))
                                     | (Q(receiver=request_user) & Q(sender=user)))
    
    return info_template(request,objects=objects, pagination_size=20, section="messages_l2",form=form)

