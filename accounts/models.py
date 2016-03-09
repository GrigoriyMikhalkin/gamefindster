from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID

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
    age = models.PositiveSmallIntegerField(null=True)
    sex = models.NullBooleanField(null=True) # M -- True, F -- False
    residence = models.CharField(max_length=128,default="")
    status_message = models.CharField(max_length=128,default="")
    steamid = models.CharField(max_length=128,null=True)
    currentpic = models.OneToOneField(UserPic,on_delete=models.SET_NULL,null=True)

class UserSettings(models.Model):
    user = models.OneToOneField(User,related_name="settings")

    """
    page_privacy_setting
    message_senders_setting
    """
    
class Language(models.Model):
    pass


class LanguageToUser(models.Model):
    pass 
