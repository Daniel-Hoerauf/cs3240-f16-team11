from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods


from django.shortcuts import render
from .forms import ReportForm
from django.db import models as m

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

def report_form_upload(request):
    form = ReportForm(request.REPORT)
    title = form.cleaned_data['title']
    timestamp = form.cleaned_data['timestamp']
    short_desc = form.cleaned_data['short_desc']
    long_desc = form.cleaned_data['long_desc']
    files = form.cleaned_data['files']
    private = form.cleaned_data['private']
    username = form.cleaned_data['username']
    report = m.Report.objects.create(title=title, timestamp=timestamp, short_desc=short_desc, long_desc=long_desc,
                                     files = files, private = private, username = username)

    return render(request, 'report/form.html', {
        'form': form,
    })
