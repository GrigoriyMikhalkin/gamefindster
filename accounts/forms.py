from .models import *
from registration.backends.hmac.views import ActivationView

class mActivationView(ActivationView):

    def activate(self, *args, **kwargs):
        user = super().activate(*args,**kwargs)

        if user:
            user_info = UserInfo(user=user)
            user_settings = UserSettings(user=user)
            user_info.save()
            user_settings.save()

        return user
