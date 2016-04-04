import pytz
from django.utils import timezone
from accounts.models import UserInfo


class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()


class LastActivityMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            UserInfo.objects.filter(user=request.user).update(last_active=timezone.now())
