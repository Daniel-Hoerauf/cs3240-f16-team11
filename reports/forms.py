from django import forms
from .models import Report

class ReportForm(forms.ModelForm):

    title = forms.CharField(max_length=256)
    short_desc = forms.CharField(widget=forms.Textarea)
    long_desc = forms.CharField(widget=forms.Textarea)
    files = forms.FileField(required=False)
    private = forms.BooleanField(required=False)
    username = forms.CharField(max_length = 256)

    class Meta:
        model = Report
        #fields = ('title', 'timestamp', 'short_desc', 'long_desc', 'files', 'private', 'username',)
        fields = ('title', 'short_desc', 'long_desc', 'files', 'private', 'username',)
