from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from cities.models import City
    
class Game(models.Model):
    name = models.CharField(max_length=512)
    shortcut = models.CharField(max_length=32,null=True,blank=True)
    is_shortcut = models.BooleanField(default=False)
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
    event_number = models.PositiveIntegerField(default=0)
    """
    platforms = models.ManyToManyField(
        Platform,blank=True, null=True)
    """

    def number_of_events(self):
        events = self.event_set.filter(is_full=False,before__gt=timezone.now())
        num_events = events.count()
        return num_events

    def get_name(self):
        if self.is_shortcut:
            return self.shortcut
        return self.name
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-event_number"]

    
class Platform(models.Model):
    name = models.CharField(max_length=512)
    logo = StdImageField(upload_to=UploadToUUID(path="platforms/logo/"),\
                          variations={'thumbnail': {'width':25,'height':25},
                                  })
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

    
class Event(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=512)
    owner = models.ForeignKey(User,default=None,null=True)
    platform = models.ForeignKey(Platform,null=True)
    location = models.ForeignKey(City,null=True)
    description = models.TextField()
    participant_number = models.PositiveSmallIntegerField(default=2)
    is_full = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(verbose_name=_("start time"))
    created = models.DateTimeField(auto_now_add=True,verbose_name=_("date started"))
    before = models.DateTimeField(verbose_name=_("active before"))

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
    
    
class GamePlatform(models.Model):
    game = models.ForeignKey(Game)
    platform = models.ForeignKey(Platform)

    def __unicode__(self):
        return(self.game.name + "_" + self.platform.name)
    
    def __str__(self):
        return(self.game.name + "_" + self.platform.name)


# SIGNALS
    
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save,sender=Event)
def new_event(sender,**kwargs):
    event = kwargs["instance"]
    game = event.game
    game.event_number = models.F("event_number") + 1
    game.save()
    

@receiver(post_delete,sender=Event)
def delete_event(sender,**kwargs):
    event = kwargs["instance"]
    game = event.game
    game.event_number = models.F("event_number") - 1
    game.save()
