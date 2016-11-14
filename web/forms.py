from django import forms
from .models import registrationForm

class registration_form(forms.ModelForm):
    class Meta:
        model = registrationForm
        fields = ('username', 'email', 'password',)