from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Add this
    path('accounts/', include('accounts.urls')),  # Your 2FA URLs

    path('', include('marketplace.urls')),
]
