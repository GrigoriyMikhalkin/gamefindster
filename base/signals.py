import json
import redis
from django.db.models.signals import post_save
from django.dispatch import receiver
from my_social.models import Message


@receiver(post_save, sender=Message)
def new_message(sender, **kwargs):
    redis_client = redis.StrictRedis(host='localhost',port=6379,db=0)

    message = kwargs['instance']
    receiver = message.receiver
    new_messages = receiver.unread_messages

    for session in receiver.session_set.all():
        redis_client.publish(
            'notifications.%s' % session.session_key,
            json.dumps(
                {
                    "new_messages": new_messages,
                }
            )
        )
