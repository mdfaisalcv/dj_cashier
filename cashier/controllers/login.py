from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        
        user = authenticate(request, username=uid, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Set session variables as expected by the layout
            request.session['cid'] = 'CASHIER'
            request.session['user_id'] = user.username
            request.session['user_type'] = 'Admin' if user.is_staff else 'User'
            request.session['email'] = user.email
            
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('cashier:dashboard')
        else:
            messages.error(request, "Invalid User ID or password.")
            
    return render(request, 'login/index.html')

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('cashier:login')
