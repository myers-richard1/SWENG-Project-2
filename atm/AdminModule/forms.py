from django import forms

class LoginForm(forms.Form):
    admin_id = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16)

class CreateCardForm(forms.Form):
    account_number = forms.CharField(max_length=20)
