from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomLogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('sell/', views.sell_view, name='sell'),
    path('about/', views.about, name='about'),

    # Custom login view
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='account_login'),

    # Custom signup view
    path('signup/', views.signup_view, name='account_signup'),

    path('sell/', views.sell_view, name='sell'),

    path('buy/<int:product_id>/', views.start_paypal_payment, name='start_paypal_payment'),

    path('purchase/<int:product_id>/', views.purchase_product, name='purchase_product'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from .views import checkout_view, purchase_history

urlpatterns += [
    path('checkout/', checkout_view, name='checkout'),
    path('history/', purchase_history, name='purchase_history'),
]

from .views import user_sales_view

urlpatterns += [
    path('my-sales/', user_sales_view, name='my_sales'),
]

from .views import paypal_success_view

urlpatterns += [
    path('paypal-success/', paypal_success_view, name='paypal_success'),
]