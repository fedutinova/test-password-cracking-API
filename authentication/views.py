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


@api_view(['POST'])
def get_token_with_creds(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({"message": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    basic_auth_token = generate_basic_auth_header(username, password)

    return Response(
        {"Authorization": basic_auth_token},
        status=status.HTTP_200_OK
    )


def generate_basic_auth_header(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return f"Basic {token}"