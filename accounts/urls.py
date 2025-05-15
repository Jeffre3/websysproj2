# accounts/urls.py
from django.urls import path
from .views import login_view, enter_email_for_2fa, verify_2fa_code

urlpatterns = [
    path('login/', login_view, name='login'),
    path('enter-email/', enter_email_for_2fa, name='enter_email_for_2fa'),
    path('verify-2fa/', verify_2fa_code, name='verify_2fa_code'),
]
    