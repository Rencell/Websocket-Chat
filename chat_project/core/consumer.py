import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async, sync_to_async

from core.models import Room

class ChatConsumer(AsyncWebsocketConsumer):
    

    async def connect(self):
        self.room = "try"

        
        await self.channel_layer.group_add(
            self.room, self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room, self.channel_name
        )

        return await super().disconnect(code)
    

    async def receive(self, text_data=None, bytes_data=None):
        json_my_text = json.loads(text_data)
        message = json_my_text["chat_message"]

        await self.channel_layer.group_send(
            self.room,
            {   
                "type": "chat_message",
                "message" : message,
                "username" : "fucker"
            }
        )


        
    async def chat_message(self,event):
        message = event["message"]
        user = event["username"]

        message_html = f"<div hx-swap-oob='beforeend:#chat_room'><p><b>{user}</b>: {message}</p></div>"

        await self.send(
            text_data=json.dumps(
                {
                    "message": message_html
                }
            )
        )
    