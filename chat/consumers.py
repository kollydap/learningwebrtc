from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "Test-Room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("disconnected")

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        message = receive_dict["message"]
        await self.channel_layer.group_send(
            {"type": "send.message", "message": message}
        )

    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
