from .models import *

def add_additional_user_models(user,*args,**kwargs):
    try:
        UserInfo.objects.get(user=user)
    except UserInfo.DoesNotExist:
        user_info = UserInfo(user=user)
        user_settings= UserSettings(user=user)
        search_settings = UserSearchSettings(user=user)
        user_info.save()
        user_settings.save()
        search_settings.save()

def populate_user_info():
    pass
