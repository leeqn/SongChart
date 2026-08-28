from django.shortcuts import render

def index(request):
    return render(request,'main/index.html')

def scrobbles(request):
    return render(request,'main/scrobbles.html')

def analytics(request):
    return render(request,'main/analytics.html')

def settings(request):
    return render(request,'main/settings.html')