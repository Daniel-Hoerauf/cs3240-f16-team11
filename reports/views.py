from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Report, UploadedFile, Folder
from .forms import ReportForm, FolderForm
from django.template import RequestContext
from web.models import UserGroup
from django.contrib.auth.models import User
from Crypto import Random
from datetime import datetime
# Create your views here.
random_generator = Random.new().read

def index(request):
    return render(request, 'createReport.html')
def thanks(request):
    return render(request, 'form.html')


def folders(request):
    reports = Report.objects.all()
    folders = Folder.objects.all()
    return render(request, 'reports/folders.html', {'folders': folders})

def viewReportsInFolders(request):
    folders = Folder.objects.all()
    reports = Report.objects.all()

    return render(request, 'reports/savedReports.html',
                  {'folders': folders, 'reports': reports})

def create_folder(request):
    reports = Report.objects.all()
    username_id = request.user
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES)
        selected = request.POST.getlist('selected_report[]')
        if form.is_valid():
            folder_object = Folder.objects.create(
                name=form.cleaned_data['title'], owner=username_id
            )
            for report_selected in selected:
                re = Report.objects.get(title=report_selected)
                folder_object.members.add(re)
        return HttpResponse("Folder has been created")


    else:
        form = FolderForm()
    variables = RequestContext(request, {
        'form': form, 'reports': reports
    })

    return render_to_response(
        'reports/folderz.html',
        variables,
    )



def folder(request):
    folder_name = request.POST.get('selected')
    print(folder_name)
    reports = Report.objects.all()
    print(reports)
    return render(request, 'reports/folder.html', {'folder_name': folder_name,
                                                   'reports': reports})


@login_required
def add_report(request):
    form_class = ReportForm(user=request.user)
    # if this is a POST request process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = ReportForm(request.POST, request.FILES, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            report = form.save(commit=False)
            report.owner = User.objects.get(username=request.user.username)
            if form.cleaned_data['Share with:'] != 'all':
                report.group = UserGroup.objects.get(
                    name=form.cleaned_data['Share with:'])
            files = request.FILES.getlist('file_field')
            report.save()
            for f in files:
                file = UploadedFile(report=report, owner=request.user)
                file.file_obj = f
                file.save()




        # redirect to a new URL:
            return render(request, 'reports/createReport.html', {'form': form_class})

        else:
            text = form.errors
            return HttpResponse(text)

    return render(request, 'reports/createReport.html', {'form': form_class})

@login_required
def edit_report(request, id=None):
    try:
        if id:
            report = Report.objects.get(pk=id)
            if report.owner != request.user:
                text = "You do not have permission to edit this report"
                return HttpResponse(text)
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
                files = request.FILES.getlist('file_field')
                report.save()
                for curr in report.file_set.all():
                    curr.delete()
                for f in files:
                    file = UploadedFile(report=report, owner=request.user)
                    file.file_obj = f
                    file.save()
                return render(request, 'reports/doneEditing.html', {'form': form_class})

            else:
                text = form.errors
                return HttpResponse(text)
    except:
        text = "You do not have permission to edit this report"
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
    for report in reports_list:
        report.files = report.file_set.all()
        for file in report.files:
            file.file_obj.name = file.file_obj.name.split('/')[-1]
    return render(request, 'reports/see_reports.html', {'reports_list':
                                                        reports_list,
                                                        'search_values':
                                                        initial_search})

def add_reports(request, folder_name):
    print("hi")
    print(folder_name)
    reports = Report.objects.all()
    username_id = request.user
    print(request.method)
    if request.method == 'POST':
        print("hi2")
        form = FolderForm(request.POST)
        selected = request.POST.getlist('selectedReport[]')
        print(selected)
        if form.is_valid():
            print("hi3")
            folder_object = Folder.objects.create(name=folder_name,
                                                  owner=username_id)
            folder_object.save()
            for report_selected in selected:
                re = Report.objects.get(title=report_selected)
                folder_object.members.add(re)
            print(folder_object.members)


    else:
        form = FolderForm()
        folder_object = []
        if folder_name is not None:
            folder_object = Folder.objects.get(name=folder_name)
        print(folder_object)
        print(folder_object.members)

    variables = RequestContext(request, {'form': form, 'reports': reports})

    return render_to_response(
        'reports/folder.html',
        variables,
        )


def viewFolders(request):
    context = {}
    context['folders_list'] = Folder.objects.all()
    return render(request, '/reports/folders', context)


@login_required
def see_my_reports(request):
    initial_search = {}
    my_reports_list = Report.objects.all().filter(owner=request.user).order_by('keyword')
    for group in UserGroup.objects.filter(members=request.user):
        my_reports_list = my_reports_list | group.report_set.all()
    # Filter based by min date
    if request.GET.get('sincesearch', False):
        date_in = request.GET['sincesearch']
        initial_search['since'] = date_in
        date_since = datetime(
            *[int(v) for v in date_in.replace('T', '-').replace(':',
                                                                '-').split('-')])
        my_reports_list = my_reports_list.filter(timestamp__gte=date_since)
    # Filter based by max date
    if request.GET.get('beforesearch', False):
        date_in = request.GET['beforesearch']
        initial_search['before'] = date_in
        date_since = datetime(
            *[int(v) for v in date_in.replace('T', '-').replace(':',
                                                                '-').split('-')])
        my_reports_list = my_reports_list.filter(timestamp__lte=date_since)
    # Filter based on creator
    if request.GET.get('ownersearch', False):
        owner = request.GET['ownersearch']
        initial_search['owner'] = owner
        my_reports_list = my_reports_list.filter(owner__username__icontains=owner)
    # Filter based on title
    if request.GET.get('titlesearch', False):
        title = request.GET['titlesearch']
        initial_search['title'] = title
        my_reports_list = my_reports_list.filter(title__icontains=title)
    # Filter based on descriptions
    if request.GET.get('descsearch', False):
        desc = request.GET['descsearch']
        initial_search['desc'] = desc
        short_search = my_reports_list.filter(short_desc__icontains=desc)
        long_search = my_reports_list.filter(long_desc__icontains=desc)
        my_reports_list = short_search | long_search
    for report in my_reports_list:
        report.files = report.file_set.all()
        for file in report.files:
            file.file_obj.name = file.file_obj.name.split('/')[-1]
    return render(request, 'reports/see_my_reports.html',
                  {'my_reports_list': my_reports_list, 'search_values': initial_search})

@login_required
def delete_report(request, id=None):
    try:
        report = Report.objects.get(id=id)
        if report.owner != request.user:
            text = "You do not have permission to delete this report"
            return HttpResponse(text)
        else:
            Report.objects.filter(id=id).delete()
        return render(request, 'reports/deleteReport.html')
    except:
        text = "You do not have permission to delete this report"
        return HttpResponse(text)


@login_required
def download_file(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    if file.report.group is not None:
        if file.report.group not in UserGroup.objects.filter(members=request.user):
            return HttpResponse(status=404)

    filename = file.file_obj.name.split('/')[-1]
    response = HttpResponse(file.file_obj, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
