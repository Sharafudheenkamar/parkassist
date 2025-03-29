from django.forms import ModelForm
from .models import *


class LoginTorm(ModelForm):
    class Meta:
        model= LoginTable
        fields=['Username','Password','Type']

class UserTableform(ModelForm):
    class Meta:
        model= UserTable
        fields=['Name','Email','Phone']

class Parkassistform(ModelForm):
    class Meta:
        model= Parkassist
        fields=['Name','Email','address','Phone','plat','plong']

class Slotform(ModelForm):
    class Meta:
        model= Slot
        fields=['slotid','slotlocation','slotprice']