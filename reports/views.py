from django.shortcuts import render
from django.http import HttpResponse
from .models import Report
from django.template import loader
from .forms import ReportForm
# Create your views here.

def index(request):
    return render(request, 'createReport.html')

def create(request):

    return render(request, 'createReport.html', {'form': form_class,})

def add_report(request):
    form_class = ReportForm
    # if this is a POST request process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            r = Report()
            r.title = form.cleaned_data['title']
            r.short_desc = form.cleaned_data['short_desc']
            r.long_desc = form.cleaned_data['long_desc']
            r.username = form.cleaned_data['username']
            form.save(commit = True)


        # redirect to a new URL:
            #return index(request)
            #return render(request, 'createReport.html')
            return render(request, 'createReport.html', {'form': form_class})
            #return HttpResponse('Thank you for submitting a report!')
        else:
            text = form.errors
            #print(form.errors)
            #return render(request, 'createReport.html', {'form': form_class})
            return HttpResponse(text)

    else:
        form = ReportForm()
    #return render(request, 'createReport.html', {'form': form_class})
    return render(request, 'createReport.html', {'form': form_class})
