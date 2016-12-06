from django import forms
from .models import Report, Folder
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

class FolderForm(forms.Form):
    title = forms.CharField(required=True)

    # def clean(self):
    #     folder_name = self.cleaned_data.get('title', None)
    #     if Folder.objects.filter(name=folder_name):
    #         #raise forms.ValidationError("A folder with this name already exists")
    #
    #         return self.cleaned_data
    #     else:
    #         raise forms.ValidationError("A folder with this name already exists")

    # def clean(self):
    #     try:
    #         Folder.objects.filter(name=self.cleaned_data.get('title'))
    #         # if we get this far, we have an exact match for this form's data
    #         raise forms.ValidationError("Exists already!")
    #     except Folder.DoesNotExist:
    #         # because we didn't get a match
    #         pass
    #     return self.cleaned_data
