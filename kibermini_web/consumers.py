from channels.generic.websocket import WebsocketConsumer
from kibermini_nodes.models import Nodes
import json

class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as jex:
            print("EROR JSON", jex)
            return
        if data["command"] == "get_nodes":
            l = Nodes.objects.filter(location=data["location"])
            response = {}
            response["nodes"] = {}
            for i in l:
                response["nodes"][i.id]=i.number
            self.send(json.dumps(response))