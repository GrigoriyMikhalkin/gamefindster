from django.db import models
from django.contrib.auth.models import User
from base.models import Event

# Create your models here.

"""
class UserInfo(models.Model):
    avatar_image
    status_message

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

class Participation(models.Model):
    event = models.ForeignKey(Event)
    participant = models.ForeignKey(User)
    is_host = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.event

    def __str__(self):
        return self.event
