from django.db import models

# Create your models here.

#This is the card class that will be used by the Transaction model to
#determine which accounts to affect in card-based transactions.
class Card(models.Model):
    card_number = models.CharField(max_length = 16)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    pin = models.CharField(max_length = 4)
    name = models.CharField(100)
    issue_date = models.DateField()
    expiration_date = models.DateField()
    address = models.CharField(max_length = 100) #TODO change this?
    twoFA_status = models.BooleanField(default = False)
    phone_number = models.CharField(max_length = 11)
    card_status = models.BooleanField(default = False) #TODO what is this field used for?

    def __str__(self):
        return "%s %s" % (self.name, self.card_number)

#This class represents a single account
#Transactions can be carried out by modifying the balance of an account.

class Account(models.Model):
    account_number = models.CharField(max_length = 20)
    account_number.primary_key = True
    balance = models.DecimalField(max_digits = 20, decimal_places = 10)
    name = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 11)

    def __str__(self):
        return "%s %s" % (self.name, self.account_number)

    
