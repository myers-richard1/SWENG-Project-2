from django import forms
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    pin = forms.CharField(max_length=4)
    
class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(required=True, max_digits=10, min_value=0)

class AccountCreationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off',
        'pattern':'[0-9]+', 'title':'Enter Numbers Only '}), max_length=9, min_length=9)
    pin = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off',
        'pattern':'[0-9]+', 'title':'Enter Numbers Only '}), max_length=4, min_length=4)
    address = forms.CharField(max_length=100, required=True)