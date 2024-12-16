import json
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from channels.db import database_sync_to_async, sync_to_async # type: ignore

from Accounts.models import User
from core.models import Friend,conversation
from django.template.loader import get_template
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
        user2 = await database_sync_to_async(User.objects.get)(id=int(fucker))
        
        friend = await database_sync_to_async(Friend.objects.get)(Q(user1=user, user2=user2) | Q(user2=user, user1=user2))
        created_at = await self.save_messages(friend, user, message)
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {   
                "type": "chat_message",
                "message" : message,
                "date" : created_at,
                "user" : user.username
            }
        )
        


        
    async def chat_message(self,event):
        message = event["message"]
        date = event["date"]
        user = event["user"]

        if user == self.user.username:
            message_html = get_template("core/messages/sender.html").render(
                context={"message" : message, "date": date}
            )
        else:
            message_html =  message_html = get_template("core/messages/receiver.html").render(
                context={"message" : message, "date": date}
            )
        await self.send(
            text_data= message_html
            
        )
        
    
    @sync_to_async
    def save_messages(self, friend, user, message):
        convo = conversation.objects.create(friend=friend, sender=user, message=message)
        
        return convo.created_at
        
       
        