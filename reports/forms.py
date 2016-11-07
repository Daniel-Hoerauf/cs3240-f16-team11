from django import forms

class ReportForm(forms.Form):

    title = forms.CharField(max_length = 256)
    timestamp = forms.TimeField()
    short_desc = forms.CharField(max_length = 256)
    long_desc = forms.CharField(max_length = 256)
    files = forms.CharField(max_length = 256)
    private = forms.BooleanField()
    username = forms.CharField(max_length = 256)
