from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Nodes, Schedule
import json
import django_rq
import random
import datetime
import asyncio

def manager_task(user_id, t, p, l, n):
    begin = datetime.datetime.strptime(t, "%d/%m/%y %H:%M")
    end = begin + datetime.timedelta(minutes=int(p))
    key = "".join([str(random.randint(0, 9)) for _ in range(4)])

    user = User.objects.get(pk=user_id)
    sum = int(p) * 2
    if user.profile.money < sum:
        print("error money")
    computer = Nodes.objects.get(location=l, number=n)
    for i in Schedule.objects.filter(node=computer):
        if i.begin.date() == begin.date():
            if (i.begin.time() <= begin.time() and i.end.time() >= begin.time()) or\
                    (i.begin.time() <= end.time() and i.end.time() >= end.time()):
                        return "no free"
            if i.begin.time() >= begin.time() and i.end.time() <= end.time():
                return "no free"

    schedule = Schedule(node=computer, user=user, begin=begin, end=end, key=key)
    schedule.save()

    queue = django_rq.get_queue('default')
    queue.enqueue_at(begin - datetime.timedelta(minutes=0), start_play, schedule.id)
    queue.enqueue_at(end, stop_play, schedule.id)
    return "ok"

def start_play(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(schedule.node.channel_name, {"type": "chat_message", "text": "start"})


def stop_play(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(schedule.node.channel_name, {"type": "chat_message", "text": "stop"})


class NodeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.nodes.on = False
        self.channel_name = ""
        self.nodes.save()
        async_to_sync(self.channel_layer.group_discard)("all", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.nodes.location, self.channel_name)

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

    def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        self.send(text_data=event["text"])