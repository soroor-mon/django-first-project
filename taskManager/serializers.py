from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from taskManager.models import Task


class TaskSerializer(serializers.ModelSerializer):
    #owner = serializers.(default=CurrentUserDefault())
    #owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'owner', 'created_at', 'updated_at']




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


