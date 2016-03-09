from .models import *

def add_additional_user_models(user,*args,**kwargs):
    try:
        UserInfo.objects.get(user=user)
    except UserInfo.DoesNotExist:
        user_info = UserInfo(user=user)
        user_settings= UserSettings(user=user)
        user_info.save()
        user_settings.save()

def populate_user_info():
    pass
