from rest_framework import serializers
from .models import *

class LoginTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginTable
        fields = ['Username', 'Password']

class UserTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTable
        fields = ['Name', 'Email', 'Phone']

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id','slotid', 'slotlocation', 'slotprice']

