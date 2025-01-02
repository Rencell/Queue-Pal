import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Room
from django.db.models import F
from channels.db import database_sync_to_async

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_slug = self.scope['url_route']['kwargs']['code']
        self.user = self.scope['user']
         
        await self.channel_layer.group_add(
            self.room_slug, self.channel_name
        )
        
        return await super().connect()
    
    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(
            self.room_slug, self.channel_name
        )

        return await super().disconnect(code)
    
    async def receive(self, text_data=None, bytes_data=None):
        
        message = json.loads(text_data)  
        hello = message["hehe"]
        if hello:
            room = await self.increment_queue()
            html_message = f"<div id='count' hx-swap-oob='true'>{room}</div>"
           
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
        Room.objects.filter(code=self.room_slug).update(
            current_serving_queue_number=F('current_serving_queue_number') + 1
        )
        updated_room = Room.objects.get(code=self.room_slug) 
        
        return updated_room.current_serving_queue_number