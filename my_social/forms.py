from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Message
        fields = [
            "text",
        ]
