from django.db import models
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID

# Import models
from django.contrib.auth.models import User
from base.models import Event
from accounts.models import UserInfo


class Friend(models.Model):
    user = models.ForeignKey(User,related_name="friends") # represents User's ID
    friend = models.ForeignKey(User,related_name="friend_set")

    def __unicode__(self):
        return self.user_id

    def __str__(self):
        return self.user_id

class Group(models.Model):
    group_name = models.CharField(max_length=128)
    description = models.TextField(default="")
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')

    def __unicode__(self):
        return self.group_name
    
    def __str__(self):
        return self.group_name

    class Meta:
        ordering = ["-created"]

    
class GroupPic(models.Model):
    group = models.ForeignKey(Group, null=True)
    avatar = StdImageField(upload_to=UploadToUUID(path="group/pic/"),\
                          variations={'thumbnail': {'width':125,'height':125,"crop":True},
                                      'large': {'width':180,'height':245,"crop":True},
                                      'xlarge': {'width':800,'height':800},
                                  })
    signing = models.CharField(max_length=256,default="")


class GroupCurrentPic(models.Model):
    group = models.OneToOneField(Group, null=True,related_name="currentpic")
    currentpic = models.OneToOneField(GroupPic,on_delete=models.SET_NULL,null=True)


class GroupParticipation(models.Model):
    group = models.ForeignKey(Group)
    participant = models.ForeignKey(User)
    admin = models.BooleanField(default=False)


class GroupEvent(models.Model):
    event = models.ForeignKey(Event)
    group = models.ForeignKey(Group)
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')
    
    class Meta:
        ordering = ["-created"]
    
    
class Participation(models.Model):
    event = models.ForeignKey(Event)
    participant = models.ForeignKey(User)
    is_host = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.event

    def __str__(self):
        return self.event

    
class Message(models.Model):
    receiver = models.ForeignKey(User, related_name="received")
    sender = models.ForeignKey(User, related_name="sended")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')
    read = models.BooleanField(default=False)

    def is_read(self):
        if self.read:
            return True

        self.read = True
        user_info = UserInfo.objects.get(user=self.receiver)
        if user_info.unread_messages:
            user_info.unread_messages = models.F("unread_messages") - 1
            user_info.save()
        self.save()
        
        return False
        
    
    class Meta:
        ordering = ["-created"]


    
class Notification(models.Model):
    sender = models.ForeignKey(User,null=True,related_name="sended_notifications")
    receiver = models.ForeignKey(User)
    type = models.CharField(max_length=64)
    label = models.CharField(max_length=256)
    text = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')

    class Meta:
        ordering = ["-created"]
    

class EventNotification(models.Model):
    notification = models.OneToOneField(Notification,related_name="event_notification")
    notification_subject = models.ForeignKey(Event)

class GroupNotification(models.Model):
    notification = models.OneToOneField(Notification,related_name="group_notification")
    notification_subject = models.ForeignKey(Group)

class FriendNotification(models.Model):
    notification = models.OneToOneField(Notification,related_name="friend_notification")
    notification_subject = models.ForeignKey(User)

class Request(models.Model):
    notification = models.OneToOneField(Notification)
    requester = models.ForeignKey(User)
        
class EventApplication(models.Model):
    request = models.OneToOneField(Request,related_name="event_application")
    request_class = models.ForeignKey(Event)

class GroupApplication(models.Model):
    request = models.OneToOneField(Request,related_name="group_application")
    request_class = models.ForeignKey(Group)

class FriendApplication(models.Model):
    request = models.OneToOneField(Request,related_name="friend_application")
    request_class = models.ForeignKey(User)    


# SIGNALS

import json
import redis
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Message)
def new_message(sender, **kwargs):
    redis_client = redis.StrictRedis(host='localhost',port=6379,db=0)

    message = kwargs['instance']
    receiver = message.receiver
    if not message.read:
        user_info = UserInfo.objects.get(user=receiver)
        user_info.unread_messages = models.F("unread_messages") + 1
        user_info.save()
    
    new_messages = receiver.info.unread_messages + 1
    
    for session in receiver.session_set.all():
        redis_client.publish(
            'notifications.%s' % session.session_key,
            json.dumps(
                {
                    "new_messages": new_messages,
                }
            )
        )
    
@receiver(post_save, sender=Notification)
def new_notification(sender, **kwargs):
    redis_client = redis.StrictRedis(host='localhost',port=6379,db=0)

    notification = kwargs['instance']
    receiver = notification.receiver

    # Update unread notifications counter
    user_info = UserInfo.objects.get(user=receiver)
    user_info.unread_notifications = models.F("unread_notifications") + 1
    user_info.save()
    
    unread_notifications = receiver.info.unread_notifications
    for session in receiver.session_set.all():
        redis_client.publish(
            'notifications.%s' % session.session_key,
            json.dumps(
                {
                    "unread_notifications": unread_notifications,
                }
            )
        )
        
@receiver(post_delete, sender=Notification)
def delete_notification(sender, **kwargs):
    notification = kwargs['instance']
    receiver = notification.receiver

    # Update unread notifications counter
    user_info = UserInfo.objects.get(user=receiver)
    user_info.unread_notifications = models.F("unread_notifications") - 1
    user_info.save()
