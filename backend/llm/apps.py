from django.apps import AppConfig


class LlmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'llm'

    # def ready(self):
    #     from llm.models.message import Message
        # for message in list(Message.objects.all()):
        #     message.delete()