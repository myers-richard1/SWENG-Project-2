from django.urls import path, include
from .views import admin_home, atm_status, create_card, admin_options

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('admin_options/', admin_options, name='admin_options'),
    path('create_card/', create_card, name='create_card'),
    path('atm_status/', atm_status, name='atm_status'),

]