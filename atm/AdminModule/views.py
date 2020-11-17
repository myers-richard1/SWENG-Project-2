from django.shortcuts import render
from .forms import LoginForm, CreateCardForm


# Create your views here.
def admin_home(request):
    context = {
        "form":LoginForm
    }
    return render(request, 'admin_home.html', context)

def admin_options(request):
    context = {


    }
    return render(request, 'admin_options.html')

def create_card(request):
    context = {
        "form":CreateCardForm

    }
    return render(request, 'create_card.html', context)

def atm_status(request):
    return render(request, 'atm_status.html')

def login_fail(request):
    return render(request, 'login_fail.html')