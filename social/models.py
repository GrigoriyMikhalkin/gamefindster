from django.db import models
from django.contrib.auth.models import User
from base.models import Event

# Create your models here.

"""
class UserInfo(models.Model):
    avatar_image
    status_message
    page_privacy_setting
    message_senders_setting

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
"""


class Friend(models.Model):
    user_id = models.PositiveIntegerField(User) # represents User's ID
    friend = models.ForeignKey(User)

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
    receiver = models.ForeignKey(User, related_name="receivers")
    sender = models.ForeignKey(User, related_name="senders")
    text = models.TextField()
    label = models.CharField(max_length=256)
    prev_message = models.ForeignKey('self', null=True)
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')

class Notification(models.Model):
    receiver = models.ForeignKey(User)
    type = models.CharField(max_length=64)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')

    class Meta:
        ordering = ["-created"]

class Request(models.Model):
    notification = models.OneToOneField(Notification)
    requester = models.ForeignKey(User)
        
class Application(models.Model):
    notification = models.OneToOneField(Request)
    event = models.ForeignKey(Event)

class GroupApplication(models.Model):
    notification = models.OneToOneField(Request)
    event = models.ForeignKey(Group)

class FriendApplication(models.Model):
    notification = models.OneToOneField(Request)
    friend = models.ForeignKey(User)    
