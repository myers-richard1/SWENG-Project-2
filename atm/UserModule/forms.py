from django import forms

class LoginForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    pin = forms.CharField(max_length=4)