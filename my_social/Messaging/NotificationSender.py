from my_social.models import *

class NotificationSender():
    def __init__(self,user,receiver):
        # Check that user is authenticated
        self.user = user
        self.receiver = receiver
        self.permission = False
        if user.is_authenticated():
            self.permission = True

    @staticmethod
    def delete_notification(notification):
        notification.delete()


class ActionNotificationSender(NotificationSender):

    def __init__(self,user,receiver):
        super().__init__(user,receiver)

    def send_notification(self):
        label = self.label
        notification = Notification(receiver=self.receiver,type=self.notification_type,label=label,text=self.text)
        notification.save()

        request = Request(notification=notification,requester=self.user)
        request.save()
    
        application = self.model_object(request=request,request_class=self.request_object)
        application.save()

    @classmethod
    def load_notification(cls,user,request,text=None):
        request_object = cls.load_request_object(request)
        receiver = request.requester
        
        inst = cls(user,receiver,request_object,text)
        if (not inst.get_host_permission()):
            return False
        
        cls.delete_notification(request.notification)
        return inst

    def pre_accept(self):
        return

    def post_accept(self):
        return
    
    def accept(self):
        if (not self.pre_accept()):
            return

        sns = self.simple_notification_sender(self.user,self.receiver,self.request_object,self.accept_label,self.text)
        sns.send_notification()
        
        self.post_accept()

    def reject(self):
        sns = self.simple_notification_sender(self.user,self.receiver,self.request_object,self.reject_label, self.text)
        sns.send_notification()
        


class SimpleEventSender(NotificationSender):

    def __init__(self,user,receiver,event,label,text=None):
        super().__init__(user,receiver)

        self.type = "event_accept"
        self.event = event
        self.label = label
        self.text = text

    def send_notification(self):
        notification = Notification(receiver=self.receiver,type=self.type,label=self.label,text=self.text)
        notification.save()
    
        application = EventNotification(notification=notification,notification_subject=self.event)
        application.save()


class SimpleFriendSender(NotificationSender):

    def __init__(self,user,receiver,friend,label,text=None):
        super().__init__(user,receiver)

        self.type = "friend_accept"
        self.friend = friend
        self.label = label
        self.text = text

    def send_notification(self):
        notification = Notification(receiver=self.receiver,type=self.type,label=self.label,text=self.text)
        notification.save()
    
        application = FriendNotification(notification=notification,notification_subject=self.friend)
        application.save()


class EventRequestSender(ActionNotificationSender):

    def __init__(self,user,receiver,event,text=None):
        super().__init__(user,receiver)

        self.text = text
        self.label = "%s wants to join your event %s" %  (self.user.username,event.name)
        self.accept_label = "You're accepted to participate in event '%s'" % event.name
        self.reject_label = "You're refused to participate in event '%s'" % event.name
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

    def __init__(self,user,receiver,friend,text=None):
        super().__init__(user,receiver)

        self.text = text
        self.label = "%s wants to be your friend" %  (self.user.username)
        self.accept_label = "%s now is your friend" % self.user.username
        self.reject_label = "%s rejected your proposal" % self.user.username
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
