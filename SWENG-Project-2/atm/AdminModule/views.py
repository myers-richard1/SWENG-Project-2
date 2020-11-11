from django.shortcuts import render, HttpResponse
from .forms import LoginForm


# Create your views here.
def admin_home(request):
    context = {
        "form":LoginForm

    }
    return render(request, 'admin_home.html', context)

def admin_options(request):
    return render(request, 'admin_options.html')

def create_card(request):
    return render(request, 'create_card.html')

def atm_status(request):
    return render(request, 'atm_status.html')