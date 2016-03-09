from django.db import models
from django.contrib.auth.models import User
from base.models import Event

# Create your models here.

class Friend(models.Model):
    user = models.ForeignKey(User,related_name="friends") # represents User's ID
    friend = models.ForeignKey(User,related_name="friend_set")

    def __unicode__(self):
        return self.user_id

    def __str__(self):
        return self.user_id

class Group(models.Model):
    group_name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, related_name="owner")

    
class GroupParticipation(models.Model):
    group = models.ForeignKey(Group)
    participant = models.ForeignKey(User)
    
    
class Participation(models.Model):
    event = models.ForeignKey(Event)
    participant = models.ForeignKey(User)
    is_host = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.event

    def __str__(self):
        return self.event

    
class Message(models.Model):
    receiver = models.ForeignKey(User, related_name="received")
    sender = models.ForeignKey(User, related_name="sended")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')

    class Meta:
        ordering = ["-created"]


    
class Notification(models.Model):
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
