from django.shortcuts import render, HttpResponse
from .forms import LoginForm


# Create your views here.
def user_home(request):
    context = {
        "form":LoginForm

    }
    return render(request, 'user_home.html', context)

def user_options(request):
    return render(request, 'user_options.html')

def withdraw(request):
    return render(request, 'withdraw.html')

def transfer(request):
    return render(request, 'transfer.html')

def login_fail(request):
    return render(request, 'login_fail.html')