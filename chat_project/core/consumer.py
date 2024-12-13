import json
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from channels.db import database_sync_to_async, sync_to_async # type: ignore

from Accounts.models import User
from core.models import Friend,conversation

from django.db.models import Q

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
        message = json_my_text["chat"]
        fucker = json_my_text["friend"]
        
        user = self.user
        username = user.username
        user2 = await database_sync_to_async(User.objects.get)(id=int(fucker))
        
        friend = await database_sync_to_async(Friend.objects.get)(Q(user1=user, user2=user2) | Q(user2=user, user1=user2))
        await self.save_messages(friend, user, message)
        

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

       
        
        if user == self.user.username:
            message_html = f"<div hx-swap-oob='beforeend:#chat_room'>\
                                <div class='ms-auto flex flex-col mb-3'>\
                                    <div class='bg-white p-3 rounded-full ms-auto'>{message}</div>\
                                    <b class='text-xs'>{user}</b>\
                                </div>\
                            </div>"
        else:
            message_html = f"<div hx-swap-oob='beforeend:#chat_room'><p><b>{user}</b>: {message}</p></div>"
        
        await self.send(
            text_data=json.dumps(
                {
                    "message": message_html
                }
            )
        )
        
    
    @sync_to_async
    def save_messages(self, friend, user, message):
        conversation.objects.create(friend=friend, sender=user, message=message)
        
       
        
    
    def view_user(self):
        # user_instance = User.objects.get(id=1)
        # self.user = user_instance.username
        # return self.user
        pass