from django.urls import path, include
from .views import user_home, user_options, withdraw, transfer, verify, create_account, account_creation_options
from .views import check_balance, process_withdrawal, process_transfer, transfer_results, withdrawal_results
from .views import login_fail

urlpatterns = [
    path('', user_home, name='home'),
    path('<int:card_num>/options/', user_options, name='options'),
    path('<int:card_num>/check_balance', check_balance, name='check_balance'),
    path('<int:card_num>/withdraw/', withdraw, name='withdraw'),
    path('<int:card_num>/process_withdrawal', process_withdrawal, name='process_withdrawal'),
    path('<int:card_num>/withdrawal_results', withdrawal_results, name='withdrawal_results'),
    path('<int:card_num>/transfer/', transfer, name='transfer'),
    path('<int:card_num>/process_transfer', process_transfer, name='process_transfer'),
    path('<int:card_num>/<int:beneficiary>/transfer_results', transfer_results, name='transfer_results'),
    path('administrator/', include('AdminModule.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('verification/', verify, name="verify"),
    path('create_account', create_account, name="create_account"),
    path('account_creation_options/', account_creation_options, name="account_creation_options"),
    path('login_fail/', login_fail, name="login_fail")
]