from django.contrib import admin

# Register your models here.
from .models import Game, Event, Platform, GamePlatform

admin.site.register(Game)
admin.site.register(Event)
admin.site.register(Platform)
admin.site.register(GamePlatform)
