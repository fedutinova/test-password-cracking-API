from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CrackedPassword
from .serializers import CrackedPasswordSerializer


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def submit_md5_hash(request):
    serializer = CrackedPasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def view_submission_history(request):
    submissions = CrackedPassword.objects.filter(user=request.user)
    serializer = CrackedPasswordSerializer(submissions, many=True)
    return Response(serializer.data)
