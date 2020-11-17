from django import forms

class LoginForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    pin = forms.CharField(max_length=4)
    
class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(required=True, max_digits=10, min_value=0)