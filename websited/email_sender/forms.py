from django import forms
from django.forms import ModelForm
from .models import  SendingDomains, SpamDomains

class UploadFileForm(forms.Form):
    file = forms.FileField()

class SendingDomainsForm(ModelForm):
    class Meta:
        model = SendingDomains
        fields = ['Domain', 'Active']

class SpamDomainsForm(ModelForm):
    class Meta:
        model = SpamDomains
        fields = ['Domain', 'Active']

