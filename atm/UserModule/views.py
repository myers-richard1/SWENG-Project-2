from django.shortcuts import render, HttpResponse, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from .forms import LoginForm
from application.models import Card, Account
import datetime
from datetime import timedelta
import decimal


# Create your views here.
#get
def user_home(request):
    context = {
        "form":LoginForm

    }
    return render(request, 'user_home.html', context)

#post
def verify(request):
    card_num = request.POST['card_number']
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponse("Invalid card number.")
    print("Redirecting...")
    return HttpResponseRedirect("/%s/options" % card_num)

#post
def create_account(request):
    #account fields: account number (auto), name, phone number, balance=0
    new_name = request.POST['name']
    new_phone_number = request.POST['phone_number']
    new_account = Account(name = new_name, phone_number = new_phone_number, balance = 10000.0)
    new_account.save()

    #card fields: card_number(auto) account num (fk), pin, 
    #   issue date, exp date, address, twoFA, phone_num, card_status
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

#get
def account_creation_options(request):
    return render(request, "account_creation_options.html")

#get
def user_options(request, card_num):
    print(card_num)
    context = {'card_num' : card_num} 
    return render(request, 'user_options.html', context)

#get
def withdraw(request, card_num):
    context = {'card_num' : card_num}
    return render(request, 'withdraw.html', context)

#post
def process_withdrawal(request, card_num):
    try:
        account = Account.objects.get(card=card_num)
    except Account.DoesNotExist:
        return HttpResponse("Could not find account")
    amount = float(request.POST['amount'])
    if (amount > account.balance):
        return HttpResponse("Account balance ($%.2f) is lower than requested amount ($%.2f). TODO implement error handler" % (account.balance, amount))
    else:
        account.balance -= decimal.Decimal(amount)
        account.save()
    #TODO create transaction record
    return HttpResponseRedirect('/%s/withdrawal_results' % card_num)

#get
def withdrawal_results(request, card_num):
    try:
        account = Account.objects.get(card = card_num)
    except Account.DoesNotExist:
        return HttpResponse("Could not find account")
    balance_str = "$%.2f" % account.balance
    context = {'card_num':card_num, 'balance':balance_str}
    return render(request, "withdrawal_results.html", context)


#get
def transfer(request, card_num):
    context = {'card_num':card_num}
    return render(request, 'transfer.html', context)

#post
def process_transfer(request, card_num):
    beneficiary = request.POST['beneficiary']
    try:
        account = Account.objects.get(pk=beneficiary)
    except Account.DoesNotExist:
        return HttpResponse("Invalid account.")
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponse("Invalid card number.")
    amount = float(request.POST['amount'])
    if (amount > card.account.balance):
        return HttpResponse("Account balance ($%.2f) is lower than requested amount ($%.2f). TODO implement error handler" % (card.account.balance, amount))
    else:
        amount_dec = decimal.Decimal(amount)
        account.balance += amount_dec
        account.save()
        card.account.balance -= amount_dec
        card.account.save()
    #TODO create transaction record
    return HttpResponseRedirect('/%s/%s/transfer_results' % (card_num, beneficiary))

#get
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

#get
def check_balance(request, card_num):
    try:
        card = Card.objects.get(pk=card_num)
    except Card.DoesNotExist:
        return HttpResponse("Invalid card number.")
    balance_str = "$%.2f" % card.account.balance
    context = {'card_num': card_num, 'balance':balance_str}
    return render(request, "check_balance.html", context)
    return HttpResponse("Balance for card %s: $%.2f" % (card_num , card.account.balance))