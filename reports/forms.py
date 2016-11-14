from django import forms
from .models import Report

class ReportForm(forms.Form):

    title = forms.CharField(max_length=256)
    timestamp = forms.TimeField()
    short_desc = forms.CharField(widget=forms.Textarea)
    long_desc = forms.CharField(widget=forms.Textarea)
    files = forms.CharField(max_length = 256)
    private = forms.BooleanField()
    username = forms.CharField(max_length = 256)

    class Report:
        model = Report
        fields = ('title', 'timestamp', 'short_desc', 'long_desc', 'files', 'private', 'username')