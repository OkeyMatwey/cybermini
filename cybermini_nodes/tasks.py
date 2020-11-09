from celery import shared_task
from cybermini.celery import app
from cybermini_nodes.models import Nodes, Schedule
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import random
import datetime

channel_layer = get_channel_layer()

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
            if (i.begin.time() <= begin.time() and i.end.time() >= begin.time()) or \
                    (i.begin.time() <= end.time() and i.end.time() >= end.time()):
                return "no free"
            if i.begin.time() >= begin.time() and i.end.time() <= end.time():
                return "no free"

    schedule = Schedule(node=computer, user=user, begin=begin, end=end, key=key)
    schedule.save()

    start_play.apply_async((schedule.id,), eta=begin-datetime.timedelta(hours=int(computer.location.time_zone)))
    stop_play.apply_async((schedule.id,), eta=end-datetime.timedelta(hours=int(computer.location.time_zone)))
    return "ok"


@shared_task
def start_play(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    async_to_sync(channel_layer.send)(schedule.node.channel_name, {"type": "chat_message", "text": {
        "create": {"username": schedule.user.username, "key": schedule.key}
    }})


@shared_task
def stop_play(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    async_to_sync(channel_layer.send)(schedule.node.channel_name, {"type": "chat_message", "text": {
        "delete": {"username": schedule.user.username}
    }})
    #schedule.delete()