# accounts/decorators.py
from django.shortcuts import redirect

def two_factor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_verified'):
            return redirect('/2fa/')
        return view_func(request, *args, **kwargs)
    return wrapper
