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

class ATMachine(models.Model):
    ATM_UID = models.AutoField(primary_key=True)
    balance = models.PositiveIntegerField()
    location = models.CharField(max_length = 100)
    minimum_balance = models.IntegerField()
    status = models.CharField(max_length = 100)
    last_refill_date = models.DateField()
    next_maintenance_date = models.DateField()

class ATM_Refill(models.Model):
    refill_ID = models.AutoField(primary_key=True)
    ATM_UID = models.ForeignKey(ATMachine, on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField()
    atm_branch = models.CharField(max_length= 100)
    refill_date = models.DateField()
    pervious_balance = models.PositiveIntegerField()

class Transaction(models.Model):
    class Meta:
        abstract= True
    transaction_id = models.AutoField(primary_key=True)
    card_number = models.ForeignKey(Card, on_delete=models.DO_NOTHING)
    date_of_transaction = models.DateField()
    ATM_UID = models.ForeignKey(ATMachine, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length= 100)
    response_code = models.IntegerField()
    transaction_type = models.CharField(max_length= 100)

class PhoneChangeTransaction(Transaction):
    new_phone_number = models.CharField(max_length=11)

class PinChangeTransaction(Transaction):
    previous_pin = models.CharField(max_length=4)
    new_pin = models.CharField(max_length=4)

class CashWithdrawalTransaction(Transaction):
    amount_transferred = models.PositiveIntegerField()
    denomination = models.CharField()
    current_balance = models.IntegerField()

class CashTransferTransaction(Transaction):
    #this is the beneficiary's account number
    account_number = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    beneficiary_name = models.CharField(max_length=100)
    amount_transferred = models.PositiveIntegerField()

class BalanceInquiryTransaction(Transaction):
    balance_amount = models.IntegerField()
    
