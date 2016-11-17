from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from django.db import models as m
from urllib.parse import quote
from .models import UserGroup

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


@require_http_methods(['GET'])
@login_required
def groups(request):
    groups = UserGroup.objects.filter(members=request.user)
    return render(request, 'web/groups.html', {'groups': groups})


@require_http_methods(['POST'])
@login_required
def create_group(request):
    group_name = request.POST.get('groupname')
    group = UserGroup(name=group_name)
    group.save()
    group.members.add(request.user)
    group.save()
    return redirect('/groups/')
    return HttpResponse(status=201)

@require_http_methods(['GET'])
@login_required
def group(request):
    group_name = request.GET['name']
    group = UserGroup.objects.get(name=group_name)
    members = []
    for member in group.members.all():
        members.append(member)
    return render(request, 'web/group.html', {'group_name': group_name,
                                              'group_members': members})
    return HttpResponse(status=200)


@require_http_methods(['POST'])
@login_required
def add_member(request):
    group_name = request.POST.get('groupname')
    group = UserGroup.objects.get(name=group_name)
    user_name = request.POST.get('username')
    user = User.objects.get(username=user_name)
    group.members.add(user)
    return redirect('/group/?name={}'.format(quote(group_name)))