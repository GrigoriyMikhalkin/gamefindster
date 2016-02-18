from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=128)
    # TODO password field
    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    
class Game(models.Model):
    name = models.CharField(max_length=512)
    cover = models.FileField(upload_to="/media/games/covers/",default="/media/games/covers/not_available.gif")
    year = models.IntegerField(blank=True, null=True)
    developer = models.CharField(
        max_length=512,blank=True, null=True)
    publisher = models.CharField(
        max_length=512,blank=True, null=True)
    """
    platforms = models.ManyToManyField(
        Platform,blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    """

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    
class Event(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=512)
    """
    description = RichTextField(blank=True, null=True)

    TODO OP user and participants
    """
    created = models.DateTimeField('date started')
    before = models.DateTimeField('active before')

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
