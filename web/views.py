from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@login_required
def home(request):
    return render(request, 'web/home.html', {})


@require_http_methods(['GET'])
def register_page(request, errors=None):
    return render(request, 'registration/register.html', {})

@require_http_methods(['POST'])
def create_account(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    user = User.objects.create_user(username, password, email)
    user.set_password(password)
    user.save()
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('/')
