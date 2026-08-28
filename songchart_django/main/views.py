import secrets
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile

@login_required(login_url='/login/')
def settings_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if not profile.api_key:
        profile.api_key = secrets.token_hex(20)
        profile.save()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'regenerate_token':
            profile.api_key=secrets.token_hex(20)
            profile.save()
            messages.success(request, 'New API Key generated successfully!')
            return redirect('settings')

        elif action == 'update_profile':
            email = request.POST.get('email')
            if email:
                request.user.email = email
                request.user.save()
                messages.success(request, 'Profile details updated!')
            return redirect('settings')

    return render(request, 'main/settings.html', {'profile': profile})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request,'main/index.html')

def scrobbles(request):
    return render(request,'main/scrobbles.html')

def analytics(request):
    return render(request,'main/analytics.html')