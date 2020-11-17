from django import forms

class LoginForm(forms.Form):
    admin_id = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16)

class CreateCardForm(forms.Form):

    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length = 100)
    phone_number = forms.CharField(max_length=11)
    account_number = forms.CharField(max_length=20)
    pin = forms.CharField(max_length=4)
    issue_date = forms.DateField()
    expiration_date = forms.DateField()
    balance = forms.DecimalField(max_digits = 20, decimal_places = 10)
    card_status = forms.CharField(max_length=10)
