"""
User admin 
"""
from llm.models.event import *
from llm.models.config import *
from llm.models.message import *
from django.contrib import admin

admin.site.register(Role)
admin.site.register(Config)
admin.site.register(Prompt)
admin.site.register(Reaction)
admin.site.register(EventFormat)

admin.site.register(Event)

admin.site.register(Message)