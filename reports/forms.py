from django import forms
from .models import Report
from web.models import UserGroup

class ReportForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['Share with:'] = forms.ChoiceField(
            choices=[('all', 'Public')] +
                    [(group.name, group.name) for group in
                     UserGroup.objects.filter(members=self.user)]
        )

    class Meta:
        model = Report
        fields = ('title', 'short_desc', 'long_desc', 'files')
