from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import LoginForm, RegisterForm


def login_required_manual(request):
    if not request.user.is_authenticated:
        return False
    return True


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'auth_functions/register.html', {'form': form})

            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth_functions/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None and user.is_active:
                login(request, user)
                return redirect('dashboard')

            form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'auth_functions/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard_view(request):
    if not login_required_manual(request):
        return redirect('login')

    return render(request, 'auth_functions/dashboard.html', {
        'user': request.user,
    })
