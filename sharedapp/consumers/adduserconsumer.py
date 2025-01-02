import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Room
from django.db.models import F
from channels.db import database_sync_to_async

class NewqueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_slug = "staff_room"
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
    
    async def staff_receive(self, event):
        html_message = event['message']
        
        await self.send(text_data=json.dumps(
            {
                'message': html_message
            }
        ))
    
   
        
  