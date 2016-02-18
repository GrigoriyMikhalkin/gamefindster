from django.contrib import admin

# Register your models here.
from .models import User, Game, Event

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Event)
