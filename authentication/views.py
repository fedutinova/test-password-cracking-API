from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from .serializers import UserSerializer
import base64


def generate_basic_auth_header(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded_credentials}"


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()

        basic_auth_token = generate_basic_auth_header(user.username, request.data['password'])

        return Response(
            {"message": "User registered successfully!", "Authorization": basic_auth_token},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"message": "Token is valid."}, status=status.HTTP_200_OK)
