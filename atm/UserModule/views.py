from django.shortcuts import render, HttpResponse, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from .forms import *
from application.models import Card, Account, CashWithdrawalTransaction, CashTransferTransaction, ATMachine
import datetime
from datetime import timedelta, date
import decimal

# Create your views here.
#GET
#this function simply displays the login page
def user_home(request):
    context = {
        "form":LoginForm
    }
    return render(request, 'user_home.html', context)

#POST
#this function accepts post data from user_home.html and 
#verifies that the credentials match what's in the database.
#on success, it redirects to user to user_options.
#on failure, it redurects to login_fail.
#POST parameters:
#   card_number:    the user's card number
#   pin:            the user's pin
def verify(request):
    card_num = request.POST['card_number']
    pin = request.POST['pin']
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponseRedirect("/login_fail/")
    if (card.pin != pin):
        return HttpResponseRedirect("/login_fail/")
    print("Redirecting...")
    return HttpResponseRedirect("/%s/options" % card_num)

#GET
#this view is basically a copy of user_home with an additional 
#error message notifying the user their attempted login was invalid
def login_fail(request):
    context = {'form':LoginForm}
    return render(request, "login_fail.html", context)

#POST
#this function accepts post data from account_creation_options.html.
#it creates both a new account, and a new card tied to that account
#POST parameters:
#   name:           the user's real name
#   phone_number:   the user's phone number
#   pin:            the user's new pin
#   address:        the user's address
def create_account(request):
    new_name = request.POST['name']
    new_phone_number = request.POST['phone_number']
    new_account = Account(name = new_name, phone_number = new_phone_number, balance = 10000.0)
    new_account.save()

    new_pin = request.POST['pin']
    new_address = request.POST['address']
    today = datetime.date.today()
    expiration = today + timedelta(365 * 4)
    new_card = Card(account=new_account, 
        pin = new_pin, issue_date=today, expiration_date=expiration,
        address = new_address, twoFA_status=False, 
        phone_number=new_account.phone_number, card_status=True)
    new_card.save()
    
    return HttpResponseRedirect('%s/options/' % new_card.card_number)

#GET
#this function simply displays the account creation form
def account_creation_options(request):
    context = {'form':AccountCreationForm}
    return render(request, "account_creation_options.html", context)

#GET
#this function verifies the card exists and then renders
#the user_options page
def user_options(request, card_num):
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        print("Card doesnt exist")
    context = {'card_num' : card_num, 'name' : "test"}
    return render(request, 'user_options.html', context)

#GET
#this function simply displays the withdrawal form
def withdraw(request, card_num):
    context = {'card_num' : card_num, 'form':WithdrawalForm}
    return render(request, 'withdraw.html', context)

#POST
#this function processes the withdrawal and updates the 
#account balance.
#POST parameters:
#   amount: the amount to withdraw from the account
def process_withdrawal(request, card_num):
    #get card and account
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponse("Could not find card")
    try:
        account = Account.objects.get(card=card_num)
    except Account.DoesNotExist:
        return HttpResponse("Could not find account")
    #get amount from POST data and update balance
    amount = float(request.POST['amount'])
    if (amount > account.balance):
        return HttpResponse("Account balance ($%.2f) is lower than requested amount ($%.2f). TODO implement error handler" % (account.balance, amount))
    else:
        account.balance -= decimal.Decimal(amount)
        account.save()
    #create transaction record
    atm = ATMachine.objects.get(pk=1)
    transaction = CashWithdrawalTransaction(card_number=card, ATM_UID=atm, status="Approved",
        date_of_transaction=date.today(), response_code="100", transaction_type="Withdrawal", amount_transferred=amount,
        denomination=".01", current_balance=account.balance)
    transaction.save()
    return HttpResponseRedirect('/%s/withdrawal_results' % card_num)

#GET
#this function simply displays the withdrawal results
def withdrawal_results(request, card_num):
    try:
        account = Account.objects.get(card = card_num)
    except Account.DoesNotExist:
        return HttpResponse("Could not find account")
    balance_str = "$%.2f" % account.balance
    context = {'card_num':card_num, 'balance':balance_str}
    return render(request, "withdrawal_results.html", context)

#GET
#this function simply displays the transfer form
def transfer(request, card_num):
    context = {'card_num':card_num}
    return render(request, 'transfer.html', context)

#POST
#this function verifies the transfer information and
#balance, and then updates the account balances.
#redirects to transfer_results
#POST parameters:
#   beneficiary:    the account number of the beneficiary account
#   amount:         the amount to transfer
def process_transfer(request, card_num):
    #get beneficiary account and user card references
    beneficiary = request.POST['beneficiary']
    try:
        account = Account.objects.get(pk=beneficiary)
    except Account.DoesNotExist:
        return HttpResponse("Invalid account.")
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponse("Invalid card number.")
    #get amount from post data update balance
    amount = float(request.POST['amount'])
    if (amount > card.account.balance):
        return HttpResponse("Account balance ($%.2f) is lower than requested amount ($%.2f). TODO implement error handler" % (card.account.balance, amount))
    else:
        #convert amount to decimal
        amount_dec = decimal.Decimal(amount)
        account.balance += amount_dec
        account.save()
        card.account.balance -= amount_dec
        card.account.save()
    #create transaction record
    atm = ATMachine.objects.get(pk=1)
    transaction = CashTransferTransaction(card_number=card, ATM_UID=atm, status="Approved",
        date_of_transaction=date.today(), response_code="100", transaction_type="Transfer",
        account_number=account, amount_transferred=amount, beneficiary_name=account.name)
    transaction.save()
    return HttpResponseRedirect('/%s/%s/transfer_results' % (card_num, beneficiary))

#GET
#this function verifies the card and beneficiary account exists,
#and renders the results of the transfer
def transfer_results(request, card_num, beneficiary):
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        HttpResponse("Invalid card number")
    try:
        account = Account.objects.get(card = card)
    except Account.DoesNotExist:
        HttpResponse("Invalid account")
    balance_str = "$%.2f" % account.balance
    context = {'card_num':card_num, 'beneficiary':beneficiary, 'balance':balance_str}
    return render(request, "transfer_results.html", context)

#GET
#this function verifies the card exists and 
#displays the balance.
def check_balance(request, card_num):
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponse("Invalid card number.")
    balance_str = "$%.2f" % card.account.balance
    context = {'card_num': card_num, 'balance':balance_str}
    return render(request, "check_balance.html", context)

#GET
#this function verifies the card exists,
#and iterates through all of the transactions involving that card,
#then adds them to the page context so they can be displayed
def view_transactions(request, card_num):
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponse("Invalid card number.")

    transfer_str = ""
    transactions_exist = False
    try:
        transactions = CashTransferTransaction.objects.filter(card_number=card)
        transactions_exist = True
        for transaction in transactions:
            transfer_str += str(transaction.amount_transferred) + "\n"
    except CashTransferTransaction.DoesNotExist:
        transfer_str += "No cash transfer transactions\n"
    
    withdrawal_str = ""
    try:
        transactions = CashWithdrawalTransaction.objects.filter(card_number=card)
        transactions_exist = True
        for transaction in transactions:
            withdrawal_str += str(transaction.amount_transferred) + "\n"
    except CashWithdrawalTransaction.DoesNotExist:
        withdrawal_str += "No cash withdrawal transactions\n"

    context = {"transfers":transfer_str, "withdrawals":withdrawal_str, "card_num":card_num}
    
    return render(request, "view_transactions.html", context)