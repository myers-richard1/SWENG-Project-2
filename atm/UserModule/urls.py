from django.urls import path, include
from .views import user_home, user_options, withdraw, transfer

urlpatterns = [
    path('', user_home, name='home'),
    path('options/', user_options, name='options'),
    path('withdraw/', withdraw, name='withdraw'),
    path('transfer/', transfer, name='transfer'),
    path('administrator/', include('AdminModule.urls')),
]