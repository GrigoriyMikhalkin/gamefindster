from django import forms
from .models import Event
from django.utils.translation import ugettext as _

class EventForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 #       self.fields["languages"].label = _("Select supported languages.(If not selected then your profile languages are set by default)")
        #self.fields["before"].widget = forms.widgets.SplitDateTimeWidget()
    
    class Meta:
        model = Event
        fields = [
            _("name"),
            _("description"),
            _("participant_number"),
            _("platform"),
            _("start_time"),
            _("before"),
        ]
