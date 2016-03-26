from django import forms
from .models import *
from accounts.models import UserPic

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Message
        fields = [
            "text",
        ]


class UserPicForm(forms.ModelForm):
    signing = forms.CharField(required=False)

    class Meta:
        model = UserPic
        fields = [
            "avatar",
            "signing",
        ]


class GroupPicForm(forms.ModelForm):
    signing = forms.CharField(required=False)

    class Meta:
        model = GroupPic
        fields = [
            "avatar",
            "signing",
        ]


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = [
            "group_name",
            "description",
        ]
