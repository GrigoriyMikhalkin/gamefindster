from datetime import datetime
from django.db import models
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
from django.utils.translation import ugettext_noop as _

# Import models
from languages_plus.models import Language
from cities.models import City
from base.models import Platform, Event
from django.contrib.auth.models import User


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
    last_active = models.DateTimeField(verbose_name="last active",null=True)
    first_time = models.BooleanField(default=True)

    def age(self):
        if self.birthdate is None:
            return None
        diff = datetime.now - birthdate.date
        return diff.year

    def is_first_time(self):
        if self.first_time:
            self.first_time = False
            self.save()
            return True

        return False

    def get_birthdate(self):
        if self.birthdate is None:
            return None
        return self.birthdate.strftime("%Y-%m-%d")

    def get_sex(self):
        if self.sex == None:
            return "Undefined"
        elif self.sex:
            return "Male"
        return "Female"
            


    
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
    platform = models.BooleanField(default=False)

    beginning = models.DateTimeField(verbose_name="beginning",null=True)
    ending = models.DateTimeField(verbose_name="ending",null=True)

    def get_beginning_date(self):
        if self.beginning is None:
            return None
        return self.beginning.strftime("%Y-%m-%d %H:%M")

    def get_ending_date(self):
        if self.ending is None:
            return None
        return self.ending.strftime("%Y-%m-%d %H:%M")

class UserPlatform(models.Model):
    user = models.ForeignKey(User,related_name="platforms")
    platform = models.ForeignKey(Platform)
    search = models.BooleanField(default=False)

class LanguageToUser(models.Model):
    user = models.ForeignKey(User,related_name="languages",null=True)
    language = models.CharField(max_length=64,null=True)
    search = models.BooleanField(default=False)

    def __str__(self):
        return self.language

    def __unicode__(self):
        return self.language


class LanguageToEvent(models.Model):
    event = models.ForeignKey(Event,related_name="languages",null=True)
    language = models.CharField(max_length=64,null=True)
