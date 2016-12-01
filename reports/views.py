from django.shortcuts import render
from django.http import HttpResponse
from .models import Report
from django.template import loader
from .forms import ReportForm
from django.template import RequestContext
from web.models import UserGroup
from django.contrib.auth.models import User
# Create your views here.

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
