from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "chatroom"
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send past messages
        messages = await self.get_all_messages()
        for message in messages:
            await self.send(text_data=json.dumps(message))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data['username']
        message = data['message']

        await self.save_message(username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': username,
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message']
        }))

    @sync_to_async
    def save_message(self, username, message):
        Message.objects.create(username=username, content=message)

    @sync_to_async
    def get_all_messages(self):
        return list(Message.objects.order_by('timestamp').values('username', 'content'))
