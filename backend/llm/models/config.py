"""
Config models
"""
import uuid
from django.db import models
from utils import TITLE_LEN, report
from asgiref.sync import sync_to_async

FILE = "[llm][models][config]"
class Role(models.Model):
    name = models.CharField(max_length=26, primary_key=True, unique=True)
    objective = models.TextField(blank=True)

    def json(self):
        return {
            "name": self.name,
            "objective": self.objective,
        }

    async def ajson(self):
        return await sync_to_async(self.json)()

    def __str__(self) -> str:
        return self.name
    
class Reaction(models.Model):
    name = models.CharField(max_length=26, primary_key=True, unique=True)

    def json(self):
        return {
            "name": self.name,
        }

    async def ajson(self):
        return await sync_to_async(self.json)()

    def __str__(self) -> str:
        return self.name

class Prompt(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=50)
    format = models.JSONField(default=[
        "This is metadata for you to remember",
        "!config.context",
        "\nThese are the last",
        "!config.past_events_size",
        "events that have taken place:\n",
        "!past_events",
        "\n\nBased on these events, generate a ",
        "!reaction.name",
        "message to be said to the user. Phrase the message in a ",
        "!reaction.name",
        " manner and ensure it aligns with your objective and personality. Limit it to a sentence with at most 20 words."
    ])

    def json(self):
        return {
            "name": self.name
        }

    async def ajson(self):
        return await sync_to_async(self.json)()

    def __str__(self) -> str:
        return self.name

class EventFormat(models.Model):
    name = models.CharField(max_length=50)

    format = models.JSONField(default=[
        "!event.cash"
    ])

    def json(self):
        return {
            "name": self.name
        }

    async def ajson(self):
        return await sync_to_async(self.json)()
    

    def __str__(self) -> str:
        return self.name

class Config(models.Model):
    default_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    default_reaction = models.ForeignKey(Reaction, on_delete=models.SET_NULL, null=True)

    # event_fromat = models.ForeignKey(EventFormat, on_delete=models.SET_NULL, null=True)
    
    context = models.JSONField(blank=True, null=True)

    past_events_size = models.IntegerField(default=5)
    include_prev_conv = models.BooleanField(default=True)

    prompt = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True)

    id = models.UUIDField(primary_key=True, default="88cb3fc06b71449b9b3a029904c8820d", editable=False)
    
    def json(self):
        return {
            "id": self.id.hex,
            "context": self.context,
            "prompt": self.prompt.json(),
            # "event_format": self.event_fromat.json(),
            "default_role": self.default_role.json(),
            "past_events_size": self.past_events_size,
            "include_prev_conv": self.include_prev_conv,
            "default_reaction": self.default_reaction.json(),
        }

    async def ajson(self):
        return await sync_to_async(self.json)()
    
    def __str__(self) -> str:
        return "Configuration"