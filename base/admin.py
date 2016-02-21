from django.contrib import admin

# Register your models here.
from .models import Game, Event

admin.site.register(Game)
admin.site.register(Event)
