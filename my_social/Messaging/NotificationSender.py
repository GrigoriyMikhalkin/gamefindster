from my_social.models import *
from django.utils.translation import ugettext_noop as _

class NotificationSender():
    def __init__(self,user,receiver=None):
        # Check that user is authenticated
        self.user = user
        self.receiver = receiver
        self.permission = False
        if user.is_authenticated():
            self.permission = True

    @staticmethod
    def delete_notification(notification):
        notification.delete()

    def send_notification(self,receiver,text=None):
        notification = Notification(sender=self.user,receiver=receiver,type=self.notification_type,label=self.label,text=text)
        notification.save()
        return notification


class SimpleNotificationSender(NotificationSender):
    def __init__(self,user,notification_object,label,receiver=None):
        super().__init__(user,receiver)

        self.notification_object = notification_object
        self.label = label

    def send_notification(self,receiver,text=None):
        notification = super().send_notification(receiver,text)
        
        type_notification = self.model_object(notification=notification,notification_subject=self.notification_object)
        type_notification.save()

        
        
class ActionNotificationSender(NotificationSender):

    def __init__(self,user,receiver=None):
        super().__init__(user,receiver)

    def send_notification(self,receiver,text=None):
        notification = super().send_notification(receiver,text)

        request = Request(notification=notification,requester=self.user)
        request.save()
    
        application = self.model_object(request=request,request_class=self.request_object)
        application.save()

    @classmethod
    def load_notification(cls,user,request):
        request_object = cls.load_request_object(request)
        receiver = request.requester
        
        inst = cls(user,request_object,receiver)
        if (not inst.get_host_permission()):
            return False
        
        cls.delete_notification(request.notification)
        return inst

    def pre_accept(self):
        return

    def post_accept(self):
        return
    
    def accept(self,text=None):
        if (not self.pre_accept()):
            return

        sns = self.simple_notification_sender(self.user,self.request_object,self.accept_label)
        sns.send_notification(self.receiver,text)
        
        self.post_accept()

    def reject(self,text=None):
        sns = self.simple_notification_sender(self.user,self.request_object,self.reject_label)
        sns.send_notification(self.receiver,text)
        


class SimpleEventSender(SimpleNotificationSender):

    def __init__(self,user,event,label,receiver=None):
        super().__init__(user,event,label,receiver)

        self.notification_type = "event"
        self.model_object = EventNotification
    

class SimpleFriendSender(SimpleNotificationSender):

    def __init__(self,user,friend,label,receiver=None):
        super().__init__(user,friend,label,receiver)

        self.notification_type = "friend"
        self.model_object = FriendNotification


class SimpleGroupSender(SimpleNotificationSender):
    def __init__(self,user,friend,label,receiver=None):
        super().__init__(user,friend,label,receiver)

        self.notification_type = "group"
        self.model_object = GroupNotification
        

class EventRequestSender(ActionNotificationSender):

    def __init__(self,user,event,receiver=None):
        super().__init__(user,receiver)

        self.label = _("%(username)s wants to join your event %(eventname)s") %  {"username":self.user.username, "eventname":event.name}
        self.accept_label = _("You're accepted to participate in event '%(eventname)s'") % {"eventname":event.name}
        self.reject_label = _("You're refused to participate in event '%(eventname)s'") % {"eventname":event.name}
        self.notification_type = "event_application"
        self.request_object = event
        self.model_object = EventApplication
        self.simple_notification_sender = SimpleEventSender

    def get_application_permission(self):
        # Check that not already participant of the event
        already_participant = self.request_object.participation_set.filter(participant=self.user).exists()
        if already_participant:
            return False
        
        # Check that there is still free places
        if self.request_object.is_full:
            return False

        return self.permission

    def get_host_permission(self):
        if self.request_object.participation_set.filter(participant=self.user).exists():
            is_host = self.request_object.participation_set.get(participant=self.user).is_host
        else:
            return False

        if (not is_host):
            return False

        return self.permission

    @staticmethod
    def load_request_object(request):
        return request.event_application.request_class

    def pre_accept(self):
        if self.request_object.is_full:
            return False
        
        participation = Participation(event=self.request_object,participant=self.receiver)
        participation.save()

        return True

    def post_accept(self):
        if self.request_object.participation_set.all().count() == self.request_object.participant_number:
            self.request_object.is_full=True
            self.request_object.save()


class FriendRequestSender(ActionNotificationSender):

    def __init__(self,user,friend,receiver=None):
        super().__init__(user,receiver)

        self.label = _("%(username)s wants to be your friend") %  {"username":self.user.username}
        self.accept_label = _("%(username)s now is your friend") % {"username":self.user.username}
        self.reject_label = _("%(username)s rejected your proposal") % {"username":self.user.username}
        self.notification_type = "friend_application"
        self.request_object = friend
        self.model_object = FriendApplication
        self.simple_notification_sender = SimpleFriendSender

    def get_application_permission(self):
        # Check that users are not friends already
        is_friend = self.user.friends.filter(friend=self.receiver).exists()
        if is_friend:
            return False
        
        # Check that applicant is not in black list

        return self.permission

    def get_host_permission(self):
        if self.user != self.request_object:
            return False

        return self.permission

    @staticmethod
    def load_request_object(request):
        return request.friend_application.request_class

    def pre_accept(self):
        if self.request_object.friends.filter(friend=self.receiver):
            return False
        
        friend = Friend(user=self.request_object,friend=self.receiver)
        friend_mutual = Friend(user=self.receiver,friend=self.request_object)
        friend.save()
        friend_mutual.save()
        
        return True


class GroupRequestSender(ActionNotificationSender):
    def __init__(self,user,group,receiver=None):
        super().__init__(user,receiver)

        self.label = _("%(username)s wants to be group member") % {"username":self.user.username}
        self.accept_label = _("Now you're member of group '%(groupname)s'") % {"groupname":group.group_name}
        self.reject_label = _("%(username)s rejected your proposal") % {"username":self.user.username}
        self.notification_type = "group_application"
        self.request_object = group
        self.model_object = GroupApplication
        self.simple_notification_sender = SimpleGroupSender

    def get_application_permission(self):
        # Check that user are not member of the group
        is_member = self.user.groupparticipation_set.filter(group=self.request_object).exists()
        if is_member:
            return False
        
        # Check that applicant is not in black list

        return self.permission

    def get_host_permission(self):
        if self.user != self.request_object.owner:
            return False

        return self.permission

    @staticmethod
    def load_request_object(request):
        return request.group_application.request_class

    def pre_accept(self):
        if self.request_object.groupparticipation_set.filter(participant=self.receiver):
            return False
        
        participation = GroupParticipation(group=self.request_object,participant=self.receiver)
        participation.save()
        
        return True


class EventInviteSender(ActionNotificationSender):
    def __init__(self,user,event,receiver=None):
        super().__init__(user,receiver)
        
        self.label = _("Invitation to join event") 
        self.accept_label = _("%(username)s now participate in event '%(eventname)s'") % {"username":self.user.username,"eventname":event.name}
        self.reject_label = _("%(username)s refused to participate in event '%(eventname)s'") % {"username":self.user.username,"eventname":event.name}
        self.notification_type = "event_invitation"
        self.request_object = event
        self.model_object = EventApplication
        self.simple_notification_sender = SimpleEventSender

    def get_invitation_permission(self,receiver):
        # Check that user is not already participant of the event
        already_participant = self.request_object.participation_set.filter(participant=receiver).exists()
        if already_participant:
            return False
        
        # Check that there is still free places
        if self.request_object.is_full:
            return False

        return self.permission

    def get_host_permission(self):
        return self.permission

    def send_notification(self,receiver,text):
        if self.get_invitation_permission(receiver):
            super().send_notification(receiver,text)

    @staticmethod
    def load_request_object(request):
        return request.event_application.request_class

    def pre_accept(self):
        if self.request_object.is_full:
            return False
        
        participation = Participation(event=self.request_object,participant=self.user)
        participation.save()

        return True

    def post_accept(self):
        if self.request_object.participation_set.all().count() == self.request_object.participant_number:
            self.request_object.is_full=True
            self.request_object.save()


class GroupInviteSender(ActionNotificationSender):
    def __init__(self,user,group,receiver=None):
        super().__init__(user,receiver)
        
        self.label = _("%(username)s invites you to join group '%(groupname)s'") %  {"username":self.user.username, "groupname":group.group_name}
        self.accept_label = _("%(username)s now member of group '%(groupname)s'") % {"username":self.user.username, "groupname":group.group_name}
        self.reject_label = _("%(username)s refused to be member of group '%(groupname)s'") % {"username":self.user.username, "groupname":group.group_name}
        self.notification_type = "group_invitation"
        self.request_object = group
        self.model_object = GroupApplication
        self.simple_notification_sender = SimpleGroupSender

    def get_invitation_permission(self,receiver):
        # Check that user are not member of the group
        is_member = receiver.groupparticipation_set.filter(group=self.request_object).exists()
        if is_member:
            return False

        return self.permission

    def get_host_permission(self):
        return self.permission

    def send_notification(self,receiver,text):
        if self.get_invitation_permission(receiver):
            super().send_notification(receiver,text)

    @staticmethod
    def load_request_object(request):
        return request.group_application.request_class

    def pre_accept(self):
        if self.request_object.groupparticipation_set.filter(participant=self.user):
            return False
        
        participation = GroupParticipation(group=self.request_object,participant=self.user)
        participation.save()
        
        return True


class CancellationBroadcaster(NotificationSender):

    def __init__(self,user):
        super().__init__(user)
        self.notification_type = "cancellation"

    def get_permission_event(self,event):
        if self.user != event.owner:
            return False
        
        return self.permission

    def get_permission_group(self,group):
        if self.user != group.owner:
            return False

        return self.permission
    
    def broadcast_event(self,event,text):
        if self.get_permission_event(event):
            self.label = "Event '%s' was cancelled by it's owner" % event.name

            for participation in event.participation_set.all():
                receiver = participation.participant
                if receiver != self.user:
                    self.send_notification(receiver,text)

    def broadcast_group(self,group,text):
        if self.get_permission_group(group):
            self.label = "Group '%s' was closed by it's owner" % group.group_name

            for participation in group.groupparticipation_set.all():
                receiver = participation.participant
                if receiver != self.user:
                    self.send_notification(receiver,text)


class EventBroadcaster(SimpleEventSender):

    def __init__(self,user,event):
        label = "Message from owner of event '%s'." % event.name
        super().__init__(user,event,label)

    def get_permission(self):
        if self.user != self.notification_object.owner:
            return False
        
        return self.permission
    
    def broadcast(self,text):
        if self.get_permission():
            for participation in self.notification_object.participation_set.all():
                receiver = participation.participant
                if receiver != self.user:
                    self.send_notification(receiver,text)


class GroupBroadcaster(SimpleGroupSender):
    def __init__(self,user,group):
        label = "Message from owner of group '%s'." % group.name
        super().__init__(user,group,label)


class FriendBroadcaster(SimpleFriendSender):
    def __init__(self,user):
        label = "Message from ." % user.name
        super().__init__(user,label)
