from django.shortcuts import render
from django.http import HttpResponse
from .models import Report
from django.template import loader
from .forms import ReportForm
# Create your views here.

def index(request):
    return HttpResponse("Create a Report")

def createReport(request):

    return render(request, 'createReport.html')
def report_form(request):
    return render(request, 'report_form.html')

def create(request):
    form_class = ReportForm

    return render(request, 'createReport.html', {'form': form_class,})