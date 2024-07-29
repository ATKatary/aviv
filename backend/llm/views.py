import json
import uuid
from datetime import datetime
from llm.models.event import *
from llm.models.config import *
from llm.models.message import *
from rest_framework import status
from user.models import CustomUser
from django.shortcuts import render
from api.openai import generate_message
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils import is_subset, report, format, ERROR

FILE = "[llm][views]"
@api_view(['POST'])
def log_event(request, *args, **kwargs) -> Response:
    """
    Logs the event 

    :param request: <HttpRequest> containing 

    :return data: {id of the created chat}
    :return status:
                HTTP_201_CREATED if the chat is created successfully
                HTTP_403_FORBIDDEN if chat could not be created
                HTTP_412_PRECONDITION_FAILED if one ore more of the request fields don't meet their precondition(s)  
    """
    data = {}
    required_fields = ["uid", "name", "isVampire", "isSurvivor", "team", "cash", "inventory", "triggerTime", "trigger"]

    response_status = is_subset(required_fields, request.data.keys())
    if response_status == status.HTTP_200_OK:
        uid = request.data['uid']
        name = request.data['name']
        team = request.data['team']
        is_vampire = request.data['isVampire']
        is_survivor = request.data['isSurvivor']

        cash = request.data['cash']
        inventory = request.data['inventory']

        trigger = request.data['trigger']
        trigger_time = datetime.fromisoformat(request.data['triggerTime'])
        
        try:
            user = CustomUser.objects.get(id=uid)
        except:
            report(f"{FILE}[log_event] >> user {uid} does not exist")
            user = CustomUser.objects.create(id=uid, name=name, password="AvivPass123")
            user.save()

        event = Event.objects.create(
            user=user,  
            cash=cash, 
            inventory=inventory, 
            is_vampire=is_vampire,
            is_survivor=is_survivor, 

            trigger=trigger, 
            trigger_time=trigger_time
        )

        for member in team:
            event.team.add(member)

        event.save()

    return Response(data=data, status = response_status)

@api_view(['POST'])
def get_ai_message(request, *args, **kwargs) -> Response:
    """
    Gets a message from the AI based on the player's last x events

    :param request: <HttpRequest> containing 

    :return data: {message}
    :return status:
                HTTP_201_CREATED if the chat is created successfully
                HTTP_403_FORBIDDEN if chat could not be created
                HTTP_412_PRECONDITION_FAILED if one ore more of the request fields don't meet their precondition(s)  
    """
    data = {}
    required_fields = ["uid"]

    response_status = is_subset(required_fields, request.data.keys())
    if response_status == status.HTTP_200_OK:
        uid = request.data['uid']
        
        try:
            user = CustomUser.objects.get(id=uid)
            events = Event.objects.filter(user=user)
            prev_conv = Message.objects.filter(user=user)
            config = Config.objects.get(id="88cb3fc06b71449b9b3a029904c8820d")

            if "role" in request.data:
                report(f"{FILE}[get_ai_message] (role) >> {request.data['role']}")
                role = Role.objects.get(name=request.data['role'])
            else: role = config.default_role

            if "reaction" in request.data:
                report(f"{FILE}[get_ai_message] (reaction) >> {request.data['reaction']}")
                reaction = Reaction.objects.get(name=request.data['reaction'])
            else: reaction = config.default_reaction

            events_json = [event.json() for event in events]
            
            prev_messages = []
            if config.include_prev_conv:
                for prev_message in prev_conv:
                    prev_messages.append({"role": "user", "content": prev_message.prompt})
                    prev_messages.append({"role": "system", "content": prev_message.content})

            past_events = events_json[-config.past_events_size:]
            report(f"{FILE}[get_ai_message] (past_events) >> {past_events}")
            prompt_variables = {
                "role.name": role.name,
                "role.objective": role.objective,

                "reaction.name": reaction.name, 

                "past_events": past_events,

                "config.context": config.context, 
                "config.past_events_size": config.past_events_size,
            }

            prompt = format(config.prompt.format, prompt_variables)
            content = generate_message(role.objective, prompt, prev_messages)
            message = Message.objects.create(
                user=user, 
                role=role,
                prompt=prompt, 
                content=content,
                reaction=reaction,
                # context=config.context,
            )
            message.save()
            data['message'] = content
            report(f"{FILE}[get_ai_message] (message) >> {content}")
        except:
            report(f"{FILE}[get_ai_message] >> user {uid} does not exist", mode=ERROR, debug=True)

    return Response(data=data, status = response_status)

