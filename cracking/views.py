import string

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CrackedPassword
from .serializers import CrackedPasswordSerializer
import hashlib
from itertools import product

charset = 'aeidu'
max_length = 15


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def crack_md5_hash(request):
    serializer = CrackedPasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        target_hash = serializer.validated_data['md5_hash']
        for length in range(1, max_length + 1):
            for attempt in product(charset, repeat=length):
                attempt_string = ''.join(attempt)
                if hashlib.md5(attempt_string.encode()).hexdigest() == target_hash:
                    # Correct return point after successful crack
                    return Response({
                        "message": "Password has been cracked successfully!",
                        "cracked_password": attempt_string
                    }, status=status.HTTP_200_OK)

        # Moved this return statement outside the length loop
        return Response({
            "message": "Failed to crack the password."
        }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def view_submission_history(request):
    submissions = CrackedPassword.objects.filter(user=request.user)
    serializer = CrackedPasswordSerializer(submissions, many=True)
    return Response(serializer.data)
