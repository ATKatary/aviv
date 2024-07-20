"""
LLM models
"""
import uuid
import json
from django.db import models
from datetime import datetime
from user.models import CustomUser
from utils import TITLE_LEN, report
from asgiref.sync import sync_to_async
from django.utils.crypto import get_random_string

FILE = "[llm][models]"
class Event(models.Model):
    cash = models.FloatField(default=0)
    isVampire = models.BooleanField(default=False)
    isSurvivor = models.BooleanField(default=False)
    inventory = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ManyToManyField(CustomUser, related_name="team", blank=True)
    
    triggerTime = models.DateTimeField(default=datetime.now)
    trigger = models.CharField(blank=True, null=True, max_length=TITLE_LEN)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def json(self):
        return {
            "id": self.id.hex, 
            "team": self.team,
            # "user": self.user.json(),
            "inventory": self.inventory, 
            "isVampire": self.isVampire,
            "isSurvivor": self.isSurvivor,

            "trigger": self.trigger,
            "triggerTime": self.triggerTime.isoformat()
        }

    async def ajson(self):
        return await sync_to_async(self.json)()
    
class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    prompt = models.TextField()
    content = models.TextField()
    context = models.TextField()
    reaction = models.CharField(
        max_length=5,
        default="funny",
        choices={
            "funny": "funny",
        } 
    )

    sentTime = models.DateTimeField(default=datetime.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    def json(self):
        return {
            "id": self.id.hex,
            # "user": self.user.json(),
            "prompt": self.prompt,
            "content": self.content,
            "context": self.context,
            "reaction": self.reaction, 
            
            "sentTime": self.sentTime.isoformat()
        }

    async def ajson(self):
        return await sync_to_async(self.json)()