from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import Report, Folder
from django.template import loader
from .forms import ReportForm, FolderForm
from django.template import RequestContext
from web.models import UserGroup
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'createReport.html')
def thanks(request):
    return render(request, 'form.html')


def folders(request):
    reports = Report.objects.all()
    folders = Folder.objects.all()
    #print(Folder.objects.get(name="test1").members.all())
    return render(request, 'reports/folders.html', {'folders': folders})

def viewReportsInFolders(request):
    folders = Folder.objects.all()
    reports = Report.objects.all()

    return render(request, 'reports/savedReports.html', {'folders':folders, 'reports':reports})



def create_folder(request):
    # folder_name = request.POST.get('foldername')
    # owner = request.user
    # folder = Folder(name=folder_name, owner=owner)
    # folder.save()
    # return addReports(request, folder_name)
    #return redirect('/reports/folders/')
    #return HttpResponse(status=201)


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
        'form': form, 'reports':reports
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


def index(request):
    return render(request, 'createReport.html')
def thanks(request):
    return render(request, 'form.html')

# def create(request):

    # return render(request, 'createReport.html', {'form': form_class,})

def add_report(request):
    form_class = ReportForm(user=request.user)
    # if this is a POST request process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            report = form.save(commit=False)
            report.owner = User.objects.get(username=request.user.username)
            if form.cleaned_data['Share with:'] != 'all':
                report.group = UserGroup.objects.get(
                    name=form.cleaned_data['Share with:'])
            report.save()

        # redirect to a new URL:
            return render(request, 'createReport.html', {'form': form_class})

        else:
            text = form.errors
            return HttpResponse(text)

    return render(request, 'createReport.html', {'form': form_class})

def see_reports(request):
    template = loader.get_template('see_reports.html')
    reports_list = Report.objects.all()
    output = ', '.join([r.title for r in reports_list])
    context = RequestContext(request, {'reports_list': reports_list})
    return HttpResponse(template.render(context))


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
            #folder_name=form.cleaned_data.get('title')
            folder_object = Folder.objects.create(
            name=folder_name, owner=username_id
            )
            folder_object.save()
            for report_selected in selected:
                re = Report.objects.get(title=report_selected)
                folder_object.members.add(re)
            print(folder_object.members)


    else:
        form = FolderForm()
        folder_object=[]
        if folder_name is not None:
            folder_object=Folder.objects.get(name=folder_name)
        print(folder_object)
        print(folder_object.members)

    variables = RequestContext(request, {
    'form': form, 'reports': reports
    })

    return render_to_response(
        'reports/folder.html',
        variables,
        )


def viewFolders(request):
    context = {}
    context['folders_list'] = Folder.objects.all()
    return render(request, '/reports/folders', context)
