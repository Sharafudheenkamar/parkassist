from rest_framework import serializers
from .models import *

class LoginTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginTable
        fields = ['UserName', 'PassWord', 'type']

class UserTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTable
        fields = ['Name', 'Email', 'Phone']