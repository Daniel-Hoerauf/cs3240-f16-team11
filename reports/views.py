from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Report
from django.template import loader
from .forms import ReportForm, EditReportForm
from django.template import RequestContext
from web.models import UserGroup
from django.contrib.auth.models import User
from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64encode, b64decode
from datetime import datetime
# Create your views here.
random_generator = Random.new().read


@login_required
def add_report(request):
    form_class = ReportForm(user=request.user)
    # if this is a POST request process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST, request.FILES, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            report = form.save(commit=False)
            report.owner = User.objects.get(username=request.user.username)
            if form.cleaned_data['Share with:'] != 'all':
                report.group = UserGroup.objects.get(
                    name=form.cleaned_data['Share with:'])
            if report.file_encrypted == True:
                #open file
                file = report.files
                file_contents = file.read()
                print(file_contents)
                #encrypt contents
                key = RSA.generate(1024, random_generator)
                encrypted_data = key.publickey().encrypt(file_contents, 32)
                encoded_data = b64encode(encrypted_data[0])
                report.files = encoded_data.decode("utf-8")
                #download file with private key
                response = HttpResponse(key.exportKey(), content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=%s.pem' % file.name
                return response

            report.save()

        # redirect to a new URL:
            return render(request, 'reports/createReport.html', {'form': form_class})

        else:
            text = form.errors
            return HttpResponse(text)

    return render(request, 'reports/createReport.html', {'form': form_class})

@login_required
def edit_report(request, id=None):
    if id:
        report = Report.objects.get(pk=id)
        print(report.title)
    else:
        report = Report()
    form_class = ReportForm(user=request.user, instance=report)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report, user=request.user)
        if form.is_valid():
            report = form.save(commit=False)
            report.owner = User.objects.get(username=request.user.username)
            if form.cleaned_data['Share with:'] != 'all':
                report.group = UserGroup.objects.get(
                    name=form.cleaned_data['Share with:'])
            report.save()
            text = 'Form has been edited'
            #return HttpResponse(text)
            return render(request, 'reports/doneEditing.html', {'form': form_class})

        else:
            text = form.errors
            return HttpResponse(text)

    return render(request, 'reports/editReport.html', {'form': form_class, 'id': id})



@login_required
def see_reports(request):
    initial_search = {}
    reports_list = Report.objects.all().filter(group=None)
    for group in UserGroup.objects.filter(members=request.user):
        reports_list = reports_list | group.report_set.all()
    # Filter based by min date
    if request.GET.get('sincesearch', False):
        date_in = request.GET['sincesearch']
        initial_search['since'] = date_in
        date_since = datetime(
            *[int(v) for v in date_in.replace('T', '-').replace(':',
                                                                '-').split('-')])
        reports_list = reports_list.filter(timestamp__gte=date_since)
    # Filter based by max date
    if request.GET.get('beforesearch', False):
        date_in = request.GET['beforesearch']
        initial_search['before'] = date_in
        date_since = datetime(
            *[int(v) for v in date_in.replace('T', '-').replace(':',
                                                                '-').split('-')])
        reports_list = reports_list.filter(timestamp__lte=date_since)
    # Filter based on creator
    if request.GET.get('ownersearch', False):
        owner = request.GET['ownersearch']
        initial_search['owner'] = owner
        reports_list = reports_list.filter(owner__username__icontains=owner)
    # Filter based on title
    if request.GET.get('titlesearch', False):
        title = request.GET['titlesearch']
        initial_search['title'] = title
        reports_list = reports_list.filter(title__icontains=title)
    # Filter based on descriptions
    if request.GET.get('descsearch', False):
        desc = request.GET['descsearch']
        initial_search['desc'] = desc
        short_search = reports_list.filter(short_desc__icontains=desc)
        long_search = reports_list.filter(long_desc__icontains=desc)
        reports_list = short_search | long_search
    return render(request, 'reports/see_reports.html', {'reports_list':
                                                        reports_list,
                                                        'search_values':
                                                        initial_search})

@login_required
def see_my_reports(request):
    template = loader.get_template('reports/see_my_reports.html')
    my_reports_list = Report.objects.all().filter(owner=request.user)
    context = RequestContext(request, {'my_reports_list': my_reports_list})
    return render(request, 'reports/see_my_reports.html', {'my_reports_list':my_reports_list})

@login_required
def delete_report(request, id=None):
    report = Report.objects.get(id=id)
    if report.owner != request.user:
        text = "You do not have permission to delete this report"
        return HttpResponse(text)
    else:
        Report.objects.filter(id=id).delete()
    return render(request, 'reports/deleteReport.html')


@login_required
def download_file(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.group is not None:
        if report.group not in UserGroup.objects.filter(members=request.user):
            return HttpResponse(status=404)

    filename = report.files.name.split('/')[-1]
    response = HttpResponse(report.files, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response