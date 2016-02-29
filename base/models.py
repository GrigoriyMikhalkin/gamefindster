from django.db import models

# Create your models here.
    
class Game(models.Model):
    name = models.CharField(max_length=512)
    cover = models.FileField(upload_to="/media/games/covers/",default="/media/games/covers/not_available.gif")
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
        events = self.event_set.all()
        num_events = events.count()
        return num_events
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    
class Event(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=512)
    description = models.TextField()
    participant_number = models.PositiveSmallIntegerField(default=2)
    is_full = models.BooleanField(default=False)

    """
    TODO OP user and participants
    """
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
