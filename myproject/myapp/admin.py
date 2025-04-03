from django.contrib import admin
from .models import LoginTable, Notificationmodel, UserTable, Parkassist, Slot, Booking, Wallet, Transaction

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(Parkassist)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Notificationmodel)
