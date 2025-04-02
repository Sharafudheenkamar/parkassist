from django.db import models
from django.db import models, transaction
from django.core.exceptions import ValidationError


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
    openingtime=models.TimeField(null=True,blank=True)
    closingtime=models.TimeField(null=True,blank=True)

class Slot(models.Model):
    parkid=models.ForeignKey(Parkassist,on_delete=models.CASCADE,null=True,blank=True)
    slotid=models.CharField(max_length=100, null=True, blank=True)
    slotstatus=models.CharField(max_length=100, null=True, blank=True)
    slotprice=models.IntegerField(null=True, blank=True)
    slotlocation=models.CharField(max_length=100,null=True,blank=True)

class Booking(models.Model):
    slotid=models.ForeignKey(Slot,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    bookingdate=models.DateField(null=True,blank=True)
    bookingstarttime=models.TimeField(null=True,blank=True)
    bookingendtime=models.TimeField(null=True,blank=True)

class Wallet(models.Model):
    user=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.FloatField(null=True, blank=True)
      # Add this line

class Transaction(models.Model):
    user=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    station=models.ForeignKey(Parkassist,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.IntegerField(null=True, blank=True)
    balance=models.IntegerField(null=True, blank=True)
    transactiontype=models.CharField(max_length=100, null=True, blank=True)
    transactiondate=models.DateTimeField(auto_now_add=True,null=True, blank=True)  # Add this line
    def save(self, *args, **kwargs):
        if not self.user or self.amount is None:
            raise ValidationError("User and amount are required for transactions.")

        wallet = Wallet.objects.filter(user=self.user).first()
        if not wallet:
            raise ValidationError("Wallet does not exist for this user.")

        with transaction.atomic():  # Ensures atomic update
                if wallet.balance < self.amount:
                    raise ValidationError("Insufficient balance in wallet.")
                wallet.balance -= self.amount  # Deduct on debit

# Add on credit

                wallet.save()
                self.balance = wallet.balance  # Store updated balance in transaction record

        super().save(*args, **kwargs)


