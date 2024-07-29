"""
Config models
"""
import uuid
from django.db import models
from datetime import datetime
from user.models import CustomUser
from asgiref.sync import sync_to_async
from llm.models.config import EventFormat
from utils import TITLE_LEN, format, report

class Event(models.Model):
    cash = models.FloatField(default=0)
    wave = models.IntegerField(default=0)
    winner = models.CharField(max_length=1000, default="")
    is_vampire = models.BooleanField(default=False)
    is_survivor = models.BooleanField(default=False)
    inventory = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ManyToManyField(CustomUser, related_name="team", blank=True)
    
    trigger_time = models.DateTimeField(default=datetime.now)
    trigger = models.CharField(blank=True, null=True, max_length=TITLE_LEN)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def json(self):
        event_variables = {
            "event.cash": self.cash,
            "event.wave": self.wave,
            "event.winner": self.winner,
            "event.is_vampire": self.is_vampire,
            "event.is_survivor": self.is_survivor, 
            "event.inventory": self.inventory, 
            "event.user": self.user.name, 
            "event.team": [member.name for member in list(self.team.all())],
            "event.trigger": self.trigger, 
            "event.trigger_time": self.trigger_time.isoformat() 
        }

        try:
            event_format = EventFormat.objects.get(name=self.trigger)
        except: 
            event_format = EventFormat.objects.create(name=self.trigger)
            event_format.save()

        return format(event_format.format, event_variables)

    async def ajson(self):
        return await sync_to_async(self.json)()