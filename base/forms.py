from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields["before"].widget = forms.widgets.SplitDateTimeWidget()
    
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "before",
        ]
