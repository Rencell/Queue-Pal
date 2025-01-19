from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from channels.layers import get_channel_layer
from django.template.loader import get_template
from core.models import UserRoom, Room
from asgiref.sync import async_to_sync


@receiver(post_save, sender=UserRoom)
def send_signal(sender, instance, created, **kwargs):
    if created:
        
        
        message_html = get_template('staff/partials/queuelist.html').render(
            context={'room':instance}
        )
        message_html = message_html.replace('\n', '').replace('\r', '')
        room = "staff_room"
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room,
            {
                'type' : 'staff_receive',
                'message' : message_html
            }
        )
        
    
        
@receiver(post_save, sender=Room)
def send_tatawa(sender, instance, created, **kwargs):
    if not created:
        
        try:
            userroom = UserRoom.objects.get(room=instance,queue_number=instance.current_serving_queue_number)
        except UserRoom.DoesNotExist:
            pass
        
    
    