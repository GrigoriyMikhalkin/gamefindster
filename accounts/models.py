from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
from base.models import Platform, Event
#from django.utils.translation import ugettext_noop as _
from cities.models import City


# Create your models here.
class UserPic(models.Model):
    user = models.ForeignKey(User, null=True)
    avatar = StdImageField(upload_to=UploadToUUID(path="user/pic/"),\
                          variations={'thumbnail': {'width':125,'height':125,"crop":True},
                                      'large': {'width':180,'height':245,"crop":True},
                                      'xlarge': {'width':800,'height':800},
                                  })
    signing = models.CharField(max_length=256,default="")


class UserInfo(models.Model):
    user = models.OneToOneField(User,related_name="info")
    full_name = models.CharField(max_length=128,default="")
    birthdate = models.DateField(null=True)
    sex = models.NullBooleanField(null=True) # M -- True, F -- False

    city = models.ForeignKey(City,null=True)
    
    status_message = models.CharField(max_length=128,default="")
    steamid = models.CharField(max_length=128,null=True)
    currentpic = models.OneToOneField(UserPic,on_delete=models.SET_NULL,null=True)
    timezone = models.CharField(max_length=32,null=True)
    unread_notifications = models.PositiveSmallIntegerField(default=0)
    unread_messages = models.PositiveSmallIntegerField(default=0)

class UserSettings(models.Model):
    user = models.OneToOneField(User,related_name="settings")

    """
    page_privacy_setting
    message_senders_setting
    """


class UserSearchSettings(models.Model):
    user = models.OneToOneField(User,related_name="search_settings")
    location = models.CharField(max_length=32,default="300")
    time = models.BooleanField(default=False)
    language = models.BooleanField(default=False)

    beginning = models.DateTimeField(verbose_name="beginning",null=True)
    ending = models.DateTimeField(verbose_name="ending",null=True)
    

class UserPlatform(models.Model):
    user = models.ForeignKey(User)
    platform = models.ForeignKey(Platform)
    search = models.BooleanField(default=False)

    
class Language(models.Model):
    name = models.CharField(max_length=128,default="English")
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class LanguageToUser(models.Model):
    user = models.ForeignKey(User,related_name="languages",null=True)
    language = models.ForeignKey(Language,related_name="users",null=True)
    search = models.BooleanField(default=False)


class LanguageToEvent(models.Model):
    event = models.ForeignKey(Event,related_name="languages",null=True)
    language = models.ForeignKey(Language,related_name="events",null=True)
