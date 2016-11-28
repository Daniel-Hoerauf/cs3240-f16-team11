from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from urllib.parse import quote
from .models import UserGroup, Message
from .forms import MessageForm


@login_required
def home(request):
    user = User.objects.get(username=request.user.username)
    unread = Message.objects.filter(recipient=user).filter(read=False)
    return render(request, 'web/home.html', {'unread': len(unread)})


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
        if member != request.user:
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


@require_http_methods(['GET'])
@login_required
def message_form(request):
    recipient = request.GET['user']
    form = MessageForm()
    return render(request, 'web/message.html', {'form': form,
                                                'recipient': recipient})


@require_http_methods(['POST'])
@login_required
def send_message(request, user):
    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.read = False
        message.sender = User.objects.get(username=request.user.username)
        message.recipient = get_object_or_404(User, username=user)
        message.save()
    else:
        return redirect('message/post/?user={}'.format(user))
    return redirect('/users')


@require_http_methods(['GET'])
@login_required
def all_messages(request):
    user = User.objects.get(username=request.user.username)
    messages = user.message_to.all()
    return render(request, 'web/messages.html', {'messages': messages})


@login_required
def message_page(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        if request.POST.get('read', False):
            message.read = False
            message.save()
            return redirect('/messages/')
        elif request.POST.get('delete', False):
            message.delete()
            return redirect('/messages/')
        else:
            return HttpResponse(status=400)
    message.read = True
    message.save()
    return render(request, 'web/view_message.html', {'message': message})


@require_http_methods(['GET'])
@login_required
def find_users(request):
    query = request.GET.get('username', '')
    users = User.objects.all().filter(username__icontains=query).exclude(
        username=request.user.username)
    curr_user = User.objects.get(username=request.user.username)
    if curr_user in users:
        users.remove(curr_user)
    return render(request, 'web/user_list.html', {'user_list': users})

    return HttpResponse(status=200)


@require_http_methods(['GET'])
@login_required
def view_user(request, user):
    if user is None:
        return HttpResponse(status=404)
    # Make sure user exists
    get_object_or_404(User, username=user)
    return render(request, 'web/user.html', {'user': user})
    return HttpResponse(status=200)
