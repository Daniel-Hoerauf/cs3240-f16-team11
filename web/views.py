from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from urllib.parse import quote
from .models import UserGroup, Message
from .forms import MessageForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64encode, b64decode
from django.views.decorators.csrf import csrf_exempt
from reports.models import Report
import json
import os


random_generator = Random.new().read


@login_required
def home(request):
    user = User.objects.get(username=request.user.username)
    if user.is_active:
        unread = Message.objects.filter(recipient=user).filter(read=False)
        return render(request, 'web/home.html', {'unread': len(unread)})
    else:
        messages.add_message(request, messages.ERROR, 'You do not have permission to login. Please contact your site manager.')
        return redirect('/login/')


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
    user.is_active = True
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
    reports_list = group.report_set.all()
    for report in reports_list:
        report.files = report.file_set.all()
        for file in report.files:
            file.file_obj.name = file.file_obj.name.split('/')[-1]
    return render(request, 'web/group.html', {'group_name': group_name,
                                              'group_members': members,
                                              'reports_list': reports_list})


@require_http_methods(['POST'])
@login_required
def add_member(request):
    group_name = request.POST.get('groupname')
    user_name = request.POST.get('username')
    try:
        group = UserGroup.objects.get(name=group_name)
        user = User.objects.get(username=user_name)
        if UserGroup.objects.filter(members=user).exists():
            messages.add_message(request, messages.ERROR, 'User is already in the group. Please enter another user.')
            return redirect('/group/?name={}'.format(quote(group_name)))
        else:
            group.members.add(user)
            messages.add_message(request, messages.SUCCESS, 'User has been added.')
            return redirect('/group/?name={}'.format(quote(group_name)))
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'User does not exist. Please enter another user.')
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
        if message.encrypted:
            text = message.message
            key = RSA.generate(1024, random_generator)
            enc_data = key.publickey().encrypt(text.encode(), 32)
            message.message = b64encode(enc_data[0])
            message.save()
            return render(request, 'web/private_key.html', {'key':
                                                            key.exportKey()})
        message.save()
    else:
        return redirect('message/post/?user={}'.format(user))
    return redirect('/users')


@require_http_methods(['GET'])
@login_required
def all_messages(request):
    user = User.objects.get(username=request.user.username)
    messages = list(user.message_to.all())[::-1]
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
        elif request.POST.get('key', False):
            key = RSA.importKey(request.POST['key'].strip())
            message.message = key.decrypt(b64decode(message.message))
            message.encrypted = False
            return render(request, 'web/view_message.html', {'message': message})
        else:
            return HttpResponse(status=400)
    message.read = True
    message.save()
    return render(request, 'web/view_message.html', {'message': message})


@require_http_methods(['GET'])
@login_required
def find_users(request):
    query = request.GET.get('usersearch', '')
    users = User.objects.all().filter(username__icontains=query).exclude(
        username=request.user.username)
    curr_user = User.objects.get(username=request.user.username)
    if curr_user in users:
        users.remove(curr_user)
    return render(request, 'web/user_list.html', {'user_list': users,
                                                  'search': query})

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


@require_http_methods(['GET'])
@login_required
def site_manager(request):
    return render(request, 'web/site_manager.html', {})


@require_http_methods(['POST'])
@login_required
def give_SM_status(request):
    user_name = request.POST.get('username')
    try:
        user = User.objects.get(username=user_name)
        group = Group.objects.get(name='Site Managers')
        if UserGroup.objects.filter(members=user).exists():
            messages.add_message(request, messages.ERROR, 'User is already a site manager. Please enter another user.')
            return redirect('/site_manager/')
        else:
            group.user_set.add(user)
            messages.add_message(request, messages.SUCCESS, 'User is now a site manager.')
            return redirect('/site_manager/')
            return HttpResponse(status=201)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'User does not exist. Please enter another user.')
        return redirect('/site_manager/')


@require_http_methods(['POST'])
@login_required
def delete_member(request):
    user_name = request.POST.get('username')
    group_name = request.POST.get('groupname')
    try:
        user = User.objects.get(username=user_name)
        group = UserGroup.objects.get(name=group_name)
        check = False
        for member in group.members.filter():
            if member == user:
                group.members.remove(member)
                check = True
        if check is True:
            messages.add_message(request, messages.SUCCESS, 'User has been deleted.')
            return redirect('/group/?name={}'.format(quote(group_name)))
            return HttpResponse(status=201)
        else:
            messages.add_message(request, messages.ERROR, 'User is not part of this group. Please enter another user.')
            return redirect('/group/?name={}'.format(quote(group_name)))
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'User does not exist. Please enter another user.')
        return redirect('/group/?name={}'.format(quote(group_name)))


@require_http_methods(['POST'])
@login_required
def suspend_account(request):
    user_name = request.POST.get('username')
    try:
        user = User.objects.get(username=user_name)
        if user.is_active:
            user.is_active = False
            user.save()
            messages.add_message(request, messages.SUCCESS, 'User is now suspended.')
            return redirect('/site_manager/')
            return HttpResponse(status=201)
        else:
            messages.add_message(request, messages.ERROR, "User's account is already suspended. Please enter another user.")
            return redirect('/site_manager/')
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'User does not exist. Please enter another user.')
        return redirect('/site_manager/')


@require_http_methods(['POST'])
@login_required
def restore_account(request):
    user_name = request.POST.get('username')
    try:
        user = User.objects.get(username=user_name)
        if user.is_active:
            messages.add_message(request, messages.ERROR, "User's account is already active. Please enter another user.")
            return redirect('/site_manager/')
        else:
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'User is now active.')
            return redirect('/site_manager/')
            return HttpResponse(status=201)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'User does not exist. Please enter another user.')
        return redirect('/site_manager/')


@login_required
def SM_get_reports(request):
    user_name = request.POST.get('username')
    try:
        user = User.objects.get(username=user_name)
        reports_list = []
        user_reports = Report.objects.filter(owner=user)
        if user_reports:
            for reports in user_reports:
                reports_list.append(reports)
            return render(request, 'web/SM_manage_reports.html', {'reports_list': reports_list, 'selected_user': user_name})
        else:
            messages.add_message(request, messages.ERROR, 'User has no reports at present.')
            return redirect('/site_manager/')
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'User does not exist. Please enter another user.')
        return redirect('/site_manager/')


@require_http_methods(['POST'])
@login_required
def SM_delete_reports(request):
    try:
        # get POST variables
        chosen_reports = request.POST.getlist('reports[]')
        selected_user = request.POST.get('selected_user')
        # delete chosen reports
        for report in chosen_reports:
            report_obj = Report.objects.filter(title=report)
            report_obj.delete()
        # update selected user's reports
        reports_list = []
        user = User.objects.get(username=selected_user)
        user_reports = Report.objects.filter(owner=user)
        if user_reports:
            for report in user_reports:
                for c_report in chosen_reports:
                    if report != c_report:
                        reports_list.append(report)
        # update SM_manage_reports page
        messages.add_message(request, messages.SUCCESS, 'Messages deleted.')
        return render(request, 'web/SM_manage_reports.html', {'reports_list': reports_list})
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Error')
        return redirect('/site_manager/')


@require_http_methods(['POST'])
@csrf_exempt
def fda_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if authenticate(username=username, password=password):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


@require_http_methods(['POST'])
@csrf_exempt
def fda_view_all_files(request):
    user_name = request.POST.get('username')
    user = User.objects.get(username=user_name)

    reports_list = []
    user_reports = Report.objects.filter(owner=user)
    if user_reports:
        for report in user_reports:
            reports_list.append({'report_id': report.id, 'report_title': report.title})
        return HttpResponse(json.dumps({'reports_list': reports_list}), content_type='application/json')
    else:
        return HttpResponse(status=404)


@require_http_methods(['POST'])
@csrf_exempt
def fda_view_report_contents(request):
    report_id = request.POST.get('report_id')
    report_obj = Report.objects.get(id=report_id)
    title = str(report_obj.title)
    owner = str(report_obj.owner.username)
    short_desc = str(report_obj.short_desc)
    long_desc = str(report_obj.long_desc)
    shared_with = str(report_obj.group)
    if shared_with is None:
        shared_with = 'Public'
    timestamp = str(report_obj.timestamp)
    files_encrypted = report_obj.files_encrypted
    files = report_obj.file_set.all()
    if files:
        files = [file.file_obj.name.split('/')[-1] for file in files]
    else:
        files = 'None'
    report_info = {'title': title, 'owner': owner, 'short_desc': short_desc, 'long_desc': long_desc,
                   'shared_with': shared_with, 'timestamp': timestamp, 'files': files, 'files_encrypted': files_encrypted}
    return HttpResponse(json.dumps({'report_info': report_info}), content_type='application/json')


@require_http_methods(['POST'])
@csrf_exempt
def fda_get_files(request):
    try:
        report_id = request.POST.get('report_id')
        file_name = request.POST.get('file_name')
        report_obj = Report.objects.get(id=report_id)
        files = report_obj.file_set.all()
        print(files)
        file = None
        for f in files:
            if f.file_obj.name.split('/')[-1] == file_name:
                file = f.file_obj
                print(file)
                break
        if file is None:
            return HttpResponse(status=404)
        response = HttpResponse(file, content_type='application/plain')
        return response
    except Exception as e:
        print(e)
        return HttpResponse(status=404)
    # report_info = {'title': title, 'owner': owner, 'short_desc': short_desc, 'long_desc': long_desc,
    #                'shared_with': shared_with, 'timestamp': timestamp, 'files': files}
    # return HttpResponse(json.dumps({'report_info': report_info}), content_type='application/json')


@login_required
def edit_info(request):
    if request.method == 'GET':
        return render(request, 'web/edit_info.html', {})
    elif request.POST.get('pass', False):
        curr_pass = request.POST['current']
        if not request.user.check_password(curr_pass):
            messages.error(request, 'Incorrect password given')
            return redirect('manage_account')
        elif request.POST['new_pass'] != request.POST['new_pass_repeat']:
            messages.error(request, 'Passwords do not match')
            return redirect('manage_account')
        else:
            username = request.user.username
            request.user.set_password(request.POST['new_pass'])
            request.user.save()
            user = authenticate(username=username,
                                password=request.POST['new_pass'])
            login(request, user)
            messages.success(request, 'Successfully updated password!')
            return redirect('manage_account')
    elif request.POST.get('email', False):
        curr_pass = request.POST['password']
        if not request.user.check_password(curr_pass):
            messages.error(request, 'Incorrect password given')
            return redirect('manage_account')
        else:
            request.user.email = request.POST['new_email']
            request.user.save()
            messages.success(request, 'Successfully updated email addresss')
            return redirect('manage_account')
    else:
        return HttpResponse(status=404)

def serve_fda(request):
    from django.views.static import serve
    filepath = os.path.join(settings.STATIC_ROOT, 'fda-django.py')
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
