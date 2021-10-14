from django import forms
from django.contrib.auth.models import User
from . import models


class AuditorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

        
class AuditorForm(forms.ModelForm):
    class Meta:
        model=models.Auditor
        fields=['mobile','profile_pic','job']

        
class AuditionForm(forms.ModelForm):
    class Meta:
        model=models.DocsAudit
        fields=['id_doc','docsgroup','info','unit']
