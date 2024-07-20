"""
User views
"""
import json
from user.models import CustomUser
from rest_framework import status
from utils import is_subset, report
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

FILE = "[user][views]"
@api_view(['POST'])
def create_user(request, *args, **kwargs) -> Response:
    """
    Creates the user

    :param request: <HttpRequest> containing 

    :return status:
                HTTP_201_CREATED if the chat is created successfully
                HTTP_403_FORBIDDEN if chat could not be created
                HTTP_412_PRECONDITION_FAILED if one ore more of the request fields don't meet their precondition(s)  
    """
    data = {}
    required_fields = ["uid", "name"]

    response_status = is_subset(required_fields, request.data.keys())
    if response_status == status.HTTP_200_OK:
        uid =  request.data['uid']
        name = request.data['name']

        try:
            user = CustomUser.objects.get(id=uid)
            report(f"{FILE}[log_event] >> user {uid} already exists")
        except:
            user, _ = CustomUser.objects.create(id=uid, name=name, password="AvivPass123")
            user.save()
            report(f"{FILE}[log_event] >> user {uid} created!")

    return Response(data=data, status = response_status)

