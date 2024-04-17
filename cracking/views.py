import hashlib

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CrackedPassword
from .serializers import CrackedPasswordSerializer
from itertools import product

charset = 'aeidu'
max_length = 8


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def crack_md5_hash(request):
    serializer = CrackedPasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        target_hash = serializer.validated_data['md5_hash']
        attempt_instance = CrackedPassword(md5_hash=target_hash, user=request.user)
        for length in range(1, max_length + 1):
            for attempt in product(charset, repeat=length):
                attempt_string = ''.join(attempt)
                if hashlib.md5(attempt_string.encode()).hexdigest() == target_hash:

                    attempt_instance.cracked_password = attempt_string
                    attempt_instance.is_cracked = True
                    attempt_instance.save()
                    return Response({
                        "message": "Password has been cracked successfully!",
                        "cracked_password": attempt_string
                    }, status=status.HTTP_200_OK)

        return Response({
            "message": "Failed to crack the password."
        }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def crack_history(request):
    attempts = CrackedPassword.objects.filter(user=request.user).order_by('-submitted_at')
    return Response([{
        'md5_hash': attempt.md5_hash,
        'cracked_password': attempt.cracked_password,
        'is_cracked': attempt.is_cracked,
        'submitted_at': attempt.submitted_at,
        'user': attempt.user.username
    } for attempt in attempts], status=status.HTTP_200_OK)