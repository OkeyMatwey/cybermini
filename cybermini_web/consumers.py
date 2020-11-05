from channels.generic.websocket import WebsocketConsumer
from cybermini_nodes.models import Nodes, Schedule
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
        if "get_nodes" in data:
            l = Nodes.objects.filter(location=data["get_nodes"]["location"])
            response = {}
            response["nodes"] = {}
            for i in l:
                response["nodes"][i.id] = i.number
            self.send(json.dumps(response))
            return
        if "get_scheduler" in data:
            l = Schedule.objects.filter(node=data["get_scheduler"]["node"])
            response = {}
            response["scheduler"] = {}
            for i in l:
                response["scheduler"][i.begin.strftime("%Y-%m-%d %H:%M:%S")] = i.end.strftime("%Y-%m-%d %H:%M:%S")
            self.send(json.dumps(response))
            return