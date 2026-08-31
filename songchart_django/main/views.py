import secrets, json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Track
from .forms import RegisterForm

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
            return redirect('settings')
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
            return redirect('settings')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})

@csrf_exempt
def api_scrobble(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    api_key = request.headers.get('X-API-Key') or request.META.get('HTTP_X_API_KEY')
    if not api_key:
        return JsonResponse({'error': 'Missing X-API-Key header'}, status=401)

    try:
        profile = UserProfile.objects.get(api_key=api_key)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Invalid API Key'}, status=403)

    try:
        data = json.loads(request.body)
        title = data.get('title')
        artist = data.get('artist')

        if not title or not artist:
            return JsonResponse({'error': 'Title and Artist are required'}, status=400)

        # Сохраняем трек с привязкой к пользователю ключа
        track = Track.objects.create(
            user=profile.user,
            title=title,
            artist=artist
        )

        return JsonResponse({'status': 'success', 'track_id': track.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request,'main/index.html')

def scrobble(request):
    return render(request,'main/scrobble.html')

def analytics(request):
    return render(request,'main/analytics.html')