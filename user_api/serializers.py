from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework import permissions

class UserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = User
        fields = ['id', 'owner', 'username', 'password', 'strategies']