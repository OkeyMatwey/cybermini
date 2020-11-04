from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Nodes
import json


class NodeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("all", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.nodes.location, self.channel_name)
        self.nodes.on = False
        self.nodes.channel_name = ""
        self.nodes.save()

    def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as jex:
            print("EROR JSON", jex)
            return
        if data["token"]:
            self.nodes = Nodes.objects.get(token=data['token'])
            if self.nodes:
                self.nodes.on = True
                self.nodes.channel_name = self.channel_name
                self.nodes.save()
                async_to_sync(self.channel_layer.group_add)("all", self.channel_name)
                async_to_sync(self.channel_layer.group_add(self.nodes.location, self.channel_name))
            else:
                self.close()
        if self.nodes.on:
            pass

    async def chat_message(self, event):
        s = json.dumps(event["text"])
        print(s)
        await self.send(text_data=s)
