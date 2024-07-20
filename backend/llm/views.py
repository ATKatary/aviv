import json
import uuid
from llm.models import *
from datetime import datetime
from rest_framework import status
from user.models import CustomUser
from django.shortcuts import render
from api.openai import generate_message
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils import is_subset, report, get_or_create, ERROR

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
        isVampire = request.data['isVampire']
        isSurvivor = request.data['isSurvivor']

        cash = request.data['cash']
        inventory = request.data['inventory']

        trigger = request.data['trigger']
        triggerTime = datetime.fromisoformat(request.data['triggerTime'])
        
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
            isVampire=isVampire,
            isSurvivor=isSurvivor, 

            trigger=trigger, 
            triggerTime=triggerTime
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
    required_fields = ["uid", "reaction"]

    response_status = is_subset(required_fields, request.data.keys())
    if response_status == status.HTTP_200_OK:
        uid = request.data['uid']
        # role = request.data['role']
        reaction = request.data['reaction']

        try:
            user = CustomUser.objects.get(id=uid)
            events = Event.objects.filter(user=user)
            events_json = [event.json() for event in events]
            previous_messages = Message.objects.filter(user=user)
            
            previous_messages_content = []
            for previous_message in previous_messages:
                previous_messages_content.append({"role": "user", "content": previous_message.prompt})
                previous_messages_content.append({"role": "system", "content": previous_message.content})

            n = 5
            event_to_consider = events_json[:n]
            role = "You are Van Helsing, your objective is to slay all the vampires and help the player survive"
            prompt = f"These are the last {n} events that have taken place:\n{event_to_consider}\n\nBased on these events, generate a {reaction} message to be said to the user. Phrase the message in a {reaction} manner and ensure it aligns with your objective and personality. Limit it to a sentence with at most 20 words."

            content = generate_message(role, prompt, previous_messages_content)
            message = Message.objects.create(
                user=user, 
                prompt=prompt, 
                reaction=reaction,
                content=content,
            )
            message.save()
            data['message'] = content
            report(f"{FILE}[get_ai_message] (message) >> {content}")
        except:
            report(f"{FILE}[get_ai_message] >> user {uid} does not exist", mode=ERROR, debug=True)

    return Response(data=data, status = response_status)

