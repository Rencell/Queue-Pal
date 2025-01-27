import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Room, UserRoom
from django.db.models import F
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.template.loader import get_template

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_slug = self.scope['url_route']['kwargs']['code']
        self.user = self.scope['user']
         
        await self.channel_layer.group_add(
            self.room_slug, self.channel_name
        )
        self.timer_user_room = f'{self.room_slug}_{self.user.username}'
        await self.channel_layer.group_add(
            self.timer_user_room, self.channel_name
        )
        
        return await super().connect()
    
    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(
            self.room_slug, self.channel_name
        )
        
        await self.channel_layer.group_discard(
            self.timer_user_room, self.channel_name
        )

        return await super().disconnect(code)
    
    async def receive(self, text_data=None, bytes_data=None):
        
        message = json.loads(text_data)  
        hello = message["hehe"]
        csrf_token = message["csrfmiddlewaretoken"]
        
        if hello:
            # incrementing queue
            
            
            room = await self.increment_queue()
            if room is not None:
                try:
                    print("sap")
                    room_current_serving = room.current_serving_queue_number
                    html_message = f"<div id='count' hx-swap-oob='true'>{room_current_serving}</div>"
                    
                    userroom = await UserRoom.objects.aget(room=room, queue_number=room_current_serving)
                    get_user = await sync_to_async(lambda:userroom.user)()
                    get_issue = await sync_to_async(lambda:userroom.issue)()
                    get_status = await sync_to_async(lambda:userroom.status.pk)()
                    
                    html_message += get_template('staff/partials/roomalert.html').render({'userroom':userroom, 'userroom_status':get_status, 'csrf_token': csrf_token})
                    html_message = html_message.replace('\n', '').replace('\"', '&quot;')
                    
                    html_message += f"<div id='trykolang' hx-swap-oob='true'>Name: {get_user}</div>"
                    html_message += f"<div id='trykolangule' hx-swap-oob='true'>Issue: {get_issue}</div>"
                except UserRoom.DoesNotExist:
                    
                    html_message += get_template('staff/partials/roomalert.html').render({'csrf_token': csrf_token})
                    html_message = html_message.replace('\n', '').replace('\r', '').replace('\"', '&quot;')
            else:
                html_message = get_template('staff/partials/notification.html').render()
                html_message = html_message.replace('\n', '').replace('\r', '').replace('\"', '&quot;')
                
            
            await self.channel_layer.group_send(
                self.room_slug,
                {   
                    "type": "queue_number",
                    "message" : html_message
                }
            )
    
    async def queue_number(self, event):
        html_message = event['message']
        await self.send(text_data=json.dumps(
            {
                'message': html_message
            }
        ))
        
        
        
    @database_sync_to_async   
    def increment_queue(self):
        room = Room.objects.filter(code=self.room_slug)
        
        if room.exists:
            current_serving_queue_number = room.first().current_serving_queue_number
            userroom = UserRoom.objects.filter(room=room.first(), queue_number=current_serving_queue_number + 1).exists()
            if userroom:
                room.update(
                    current_serving_queue_number=F('current_serving_queue_number') + 1
                )
            else:
                return None
            updated_room = Room.objects.get(code=self.room_slug)
            updated_room.user = self.user
            updated_room.save()
            return updated_room