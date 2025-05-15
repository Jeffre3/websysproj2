# accounts/views.py

import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def send_2fa_code(user_email):
    code = str(random.randint(100000, 999999))  # Generate a 6-digit code
    # Store the code in the session or database
    # Here we're using session to store the code temporarily
    session_key = '2fa_code'
    session_value = {'code': code}
    session_expires_in = 300  # 5 minutes expiration
    send_mail(
        'Your 2FA Code',
        f'Your 2FA code is: {code}',
        'your_email@gmail.com',  # Sender email (configured in settings.py)
        [user_email],  # User-provided email
    )
    return session_key, session_value, session_expires_in

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the page where the user inputs their email for 2FA
            return redirect('enter_email_for_2fa')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

# accounts/views.py

def enter_email_for_2fa(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')  # The email entered by the user
        
        if user_email:
            # Send the 2FA code to the provided email address
            session_key, session_value, session_expires_in = send_2fa_code(user_email)
            request.session[session_key] = session_value
            request.session.set_expiry(session_expires_in)
            
            # Redirect to the page where the user will input the 2FA code
            return redirect('verify_2fa_code')
    
    return render(request, 'enter_email_for_2fa.html')


# accounts/views.py

def verify_2fa_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        # Retrieve the code stored in session
        stored_code = request.session.get('2fa_code', {}).get('code')

        if entered_code == stored_code:
            # If the code matches, allow access
            request.session['is_verified'] = True
            return redirect('home')  # Or wherever you want to redirect
        else:
            return render(request, 'verify_2fa_code.html', {'error': 'Invalid 2FA code'})

    return render(request, 'verify_2fa_code.html')
