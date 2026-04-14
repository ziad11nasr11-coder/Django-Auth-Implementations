from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.shortcuts import get_object_or_404

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'auth_manual/register.html', {'form': form})

            user = User(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=username,
                email=email,
                password=make_password(password),
                phone_number=form.cleaned_data['phone_number']
            )
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'auth_manual/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                form.add_error(None, 'username or password is incorrect')
                return render(request, 'auth_manual/login.html', {'form': form})

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session.set_expiry(3600)
                return redirect('dashboard')

            form.add_error(None, 'username or password is incorrect')
    else:
        form = LoginForm()

    return render(request, 'auth_manual/login.html', {'form': form})


def logout_view(request):
    request.session.flush() 
    return redirect('login')


def dashboard_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login') 

    user = get_object_or_404(User, id=user_id)
    return render(request, 'auth_manual/dashboard.html', {'user': user})