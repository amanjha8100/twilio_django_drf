from django.shortcuts import render
from dotenv import load_dotenv
import os
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
import json
from django.conf import settings
# Create your views here.

#Authentication environmental variables


@api_view(["GET","POST"])
def room(request):
    '''Creates a room on the basis of unique name provided'''
    if request.method == "POST":
        name = request.data or ''
        if name == '':
            return Response(status.HTTP_400_BAD_REQUEST)
        print(settings.TWILIO_SID)
        twilio_client = Client(settings.TWILIO_API_SID, settings.TWILIO_API_SECRET, settings.TWILIO_SID)
        room = twilio_client.video.rooms.create(type="group",unique_name=name)
        print(name)
        return Response({"room_sid":room.sid , "unique_name":room.unique_name}, status.HTTP_201_CREATED)
    return Response(status.HTTP_400_BAD_REQUEST)

@api_view(["GET","POST"])
def token(request, room):
    '''Creates an access token and grants video access with the room specified'''
    if request.method == "POST":
        identity = request.data or ''
        if identity is '':
            return Response(status.HTTP_400_BAD_REQUEST)
        token = AccessToken(settings.TWILIO_API_SID, settings.TWILIO_API_SECRET, settings.TWILIO_SID)
        token.identity = identity or 'User'
        grant = VideoGrant()
        grant.room = room
        token.add_grant(grant)

        return Response({'token':token.to_jwt().decode()}, status.HTTP_200_OK)
    return Response(status.HTTP_400_BAD_REQUEST)

