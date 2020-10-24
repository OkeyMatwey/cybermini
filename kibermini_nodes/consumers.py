from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Nodes
import json, time

class Task:
    time = time.time()
    period = time.time()
    location = ""
    computer = 1
    user = ""
    key = 1

class NodeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass
        # async_to_sync(self.channel_layer.group_discard)("all", self.channel_name)
        # async_to_sync(self.channel_layer.group_discard)(self.nodes.location, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        print(bytes_data)

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as jex:
            print("EROR JSON", jex)
            return
        if data["token"]:
            self.nodes = Nodes.objects.get(token=data['token'])
            if self.nodes:
                self.auth = True
                # async_to_sync(self.channel_layer.group_add)("all", self.channel_name)
                # async_to_sync(self.channel_layer.group_add(self.nodes.location, self.channel_name))
            else:
                self.close()
        if self.auth:
            pass