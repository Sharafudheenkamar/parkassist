from django.db import models

# Create your models here.

class LoginTable(models.Model):
    Username = models.CharField(max_length=100, null=True, blank=True)
    Password = models.CharField(max_length=100, null=True, blank=True)
    Type = models.CharField(max_length=100, null=True, blank=True)

class UserTable(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    Phone =models.IntegerField(null=True, blank=True)

class Parkassist(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    address= models.CharField(max_length=100, null=True, blank=True)
    Phone =models.IntegerField(null=True, blank=True)
    plat=models.FloatField(null=True)
    plong=models.FloatField(blank=True)

class Slot(models.Model):
    parkid=models.ForeignKey(Parkassist,on_delete=models.CASCADE,null=True,blank=True)
    slotid=models.CharField(max_length=100, null=True, blank=True)
    slotstatus=models.CharField(max_length=100, null=True, blank=True)
    slotprice=models.IntegerField(null=True, blank=True)

class Booking(models.Model):
    slotid=models.ForeignKey(Slot,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    start=models.DateTimeField(null=True, blank=True)
    end=models.DateTimeField(null=True, blank=True)

class Wallet(models.Model):
    user=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.IntegerField(null=True, blank=True)
    balance=models.IntegerField(null=True, blank=True)  # Add this line

class Transaction(models.Model):
    user=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    station=models.ForeignKey(Parkassist,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.IntegerField(null=True, blank=True)
    balance=models.IntegerField(null=True, blank=True)
    transactiontype=models.CharField(max_length=100, null=True, blank=True)
    transactiondate=models.DateTimeField(null=True, blank=True)  # Add this line




