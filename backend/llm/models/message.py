"""
Message models
"""
import uuid
import json
from django.db import models
from datetime import datetime
from user.models import CustomUser
from utils import TITLE_LEN, report
from asgiref.sync import sync_to_async
from llm.models.config import Reaction, Role

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    prompt = models.TextField()
    content = models.TextField()
    context = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    reaction = models.ForeignKey(Reaction, on_delete=models.SET_NULL, null=True)

    sent_time = models.DateTimeField(default=datetime.now)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def json(self):
        return {
            "id": self.id.hex,
            # "user": self.user.json(),
            "prompt": self.prompt,
            "content": self.content,
            "context": self.context,
            "role": self.role.json(), 
            "reaction": self.reaction.json(), 
            
            "sent_time": self.sent_time.isoformat()
        }

    async def ajson(self):
        return await sync_to_async(self.json)()
    
    def __str__(self) -> str:
        return f"{self.sent_time}"