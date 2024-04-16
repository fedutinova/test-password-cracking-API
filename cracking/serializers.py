from rest_framework import serializers
from .models import CrackedPassword


class CrackedPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrackedPassword
        fields = ['id', 'md5_hash', 'submitted_at', 'is_cracked', 'cracked_password']
        read_only_fields = ['submitted_at', 'is_cracked', 'cracked_password']
