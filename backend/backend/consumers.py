from channels.generic.websocket import AsyncWebsocketConsumer
import json


class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("votes", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("votes", self.channel_name)

    async def vote_update(self, event):
        message = event["message"]
        await self.send(text_data=message)
