from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from .forms import registration_form

@login_required
def home(request):
    return render(request, 'web/home.html', {})

@require_http_methods(['GET'])
def register_page(request, errors=None):
    form = registration_form
    return render(request, 'registration/register.html', {'form': form})

@require_http_methods(['POST'])
def create_account(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    try:
        user = User.objects.create_user(username, password, email)
    except IntegrityError:
        error(request, 'That username has already been taken')
        return redirect('/register/')
    user.set_password(password)
    user.save()
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('/')
