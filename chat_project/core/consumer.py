import json
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from channels.db import database_sync_to_async, sync_to_async # type: ignore

from core.models import Room,Message
from Accounts.models import User

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f'chat_{self.room_slug}'
        self.user = self.scope['user']
        
        
        # hey = await database_sync_to_async(self.view_user)()
        
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

        return await super().disconnect(code)
    

    async def receive(self, text_data=None, bytes_data=None):
        
        json_my_text = json.loads(text_data)
        message = json_my_text["chat_messages"]
        user = self.user
        username = user.username
        room = self.room_slug
        
        await self.save_messages(room, user, message)
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {   
                "type": "chat_message",
                "message" : message,
                "username" : username
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
    
    @sync_to_async
    def save_messages(self, room, user, message):
        room = Room.objects.get(slug=room)
        Message.objects.create(message=message, user=user, room=room)
        print("Saved")
        
    
    def view_user(self):
        user_instance = User.objects.get(id=1)
        self.user = user_instance.username
        return self.user