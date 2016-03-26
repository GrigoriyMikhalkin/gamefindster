from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
    
class Game(models.Model):
    name = models.CharField(max_length=512)
    cover = StdImageField(upload_to=UploadToUUID(path="games/covers/"),\
                          variations={'thumbnail': {'width':100,'height':100,"crop":True},
                                      'large': {'width':400,'height':400,"crop":True},
                                  })
    year = models.IntegerField(blank=True, null=True)
    developer = models.CharField(
        max_length=512,blank=True, null=True)
    publisher = models.CharField(
        max_length=512,blank=True, null=True)
    description = models.TextField()
    """
    platforms = models.ManyToManyField(
        Platform,blank=True, null=True)
    """

    def number_of_events(self):
        events = self.event_set.filter(is_full=False,before__gt=timezone.now())
        num_events = events.count()
        return num_events
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    
class Event(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=512)
    owner = models.ForeignKey(User,default=None,null=True)
    description = models.TextField()
    participant_number = models.PositiveSmallIntegerField(default=2)
    is_full = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(verbose_name="start time")
    created = models.DateTimeField(auto_now_add=True,verbose_name='date started')
    before = models.DateTimeField(verbose_name='active before')

    def isActive(self):
        """
        Check if Event is still active
        """
        return(self.before >= timezone.now())

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created"]
        verbose_name = _('event')
        verbose_name_plural = _('events')


class Platform(models.Model):
    name = models.CharField(max_length=512)
    logo = StdImageField(upload_to=UploadToUUID(path="platforms/logo/"),\
                          variations={'thumbnail': {'width':25,'height':25},
                                  })
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    
class GamePlatform(models.Model):
    game = models.ForeignKey(Game)
    platform = models.ForeignKey(Platform)

    def __unicode__(self):
        return(self.game.name + "_" + self.platform.name)
    
    def __str__(self):
        return(self.game.name + "_" + self.platform.name)
