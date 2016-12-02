from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Report
from django.template import loader
from .forms import ReportForm
from django.template import RequestContext
from web.models import UserGroup
from django.contrib.auth.models import User
# Create your views here.


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
            report.save()

        # redirect to a new URL:
            return render(request, 'createReport.html', {'form': form_class})

        else:
            text = form.errors
            return HttpResponse(text)

    return render(request, 'createReport.html', {'form': form_class})


def get_file_dest(instance, filename):
    return 'user_{}/{}/{}/{}'.format(instance.owner.pk, instance.timestamp.minute,
                                     instance.timestamp.second, filename)

@login_required
def see_reports(request):
    query = request.GET.get('search', '')
    template = loader.get_template('see_reports.html')
    reports_list = Report.objects.all().filter(group=None)
    for group in UserGroup.objects.filter(members=request.user):
        reports_list = reports_list | group.report_set.all()
        # reports_list += group.report_set.all()
    output = ', '.join([r.title for r in reports_list])
    context = RequestContext(request, {'reports_list': reports_list})
    return HttpResponse(template.render(context))


@login_required
def download_file(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.group is not None:
        if report.group not in UserGroup.objects.filter(members=request.user):
            return HttpResponse(status=404)
    response = HttpResponse(report.file, content_type='text/plain')
    # response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
