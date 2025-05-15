from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Sale, Purchase
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from allauth.account.views import LogoutView
from .recommendations import ProductRecommender
import urllib.parse
import json


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        return "https://www.paypal.com/logout"


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def marketplace(request):
    products = Product.objects.filter(is_sold=False)
    recommender = ProductRecommender()
    
    # Get recommendations based on user's authentication status
    if request.user.is_authenticated:
        recommended_products = recommender.get_user_recommendations(request.user)
    else:
        recommended_products = recommender.get_popular_products()
    
    context = {
        'products': products,
        'recommended_products': recommended_products,
    }
    return render(request, 'marketplace.html', context)


@login_required
def sell_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            Sale.objects.create(seller=request.user, item_name=product.name, price=product.price)
            return redirect('marketplace')
    else:
        form = ProductForm()
    return render(request, 'sell.html', {'form': form})


def start_paypal_payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    paypal_base_url = "https://www.paypal.com/cgi-bin/webscr"

    params = {
        "cmd": "_xclick",
        "business": "sb-k5dki34421835@business.example.com",
        "item_name": product.name,
        "amount": product.price,
        "currency_code": "USD",
        "notify_url": "https://yourdomain.com/paypal-ipn/",
        "return": "https://yourdomain.com/paypal-success/",
        "cancel_return": "https://yourdomain.com/marketplace"
    }

    url = f"{paypal_base_url}?{urllib.parse.urlencode(params)}"
    return redirect(url)


@csrf_protect
@login_required
def purchase_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            Purchase.objects.create(user=request.user, product=product)
            product.is_sold = True
            product.save()
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def checkout_view(request):
    if request.method == 'POST':
        item = request.POST.get('item_name')
        quantity = int(request.POST.get('quantity', 1))
        price = float(request.POST.get('price', 0))
        Purchase.objects.create(user=request.user, item_name=item, quantity=quantity, price=price)
        return redirect('purchase_history')
    return render(request, 'checkout.html')


@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    return render(request, 'purchase_history.html', {'purchases': purchases})


@login_required
def user_sales_view(request):
    sales = Sale.objects.filter(seller=request.user).order_by('-listed_at')
    return render(request, 'user_sales.html', {'sales': sales})


@login_required
def paypal_success_view(request):
    item = request.GET.get('item')
    price = float(request.GET.get('price', 0))
    quantity = 1
    if item and price:
        Purchase.objects.create(user=request.user, item_name=item, quantity=quantity, price=price)
    return redirect('purchase_history')
