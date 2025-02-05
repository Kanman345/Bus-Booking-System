from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser

DEFAULT_USER_TYPE = 'passenger'  

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        user_type = request.POST['user_type']  # Get user type from form

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already used')
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        # Create user with selected user type
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        user.save()
        login(request, user)  

        # Redirect based on user role
        if user_type == 'admin':
            return redirect('admin_dashboard')
        return redirect('passenger_dashboard')

    return render(request, 'register.html')



def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both fields are required')
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('admin_dashboard' if user.user_type == 'admin' else 'passenger_dashboard')

        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username does not exist')
        else:
            messages.error(request, 'Incorrect password')

        return redirect('login')

    return render(request, 'login.html')


