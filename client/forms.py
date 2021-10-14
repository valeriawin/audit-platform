from django import forms
from django.contrib.auth.models import User
from . import models


class ClientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

        
class ClientForm(forms.ModelForm):
    class Meta:
        model=models.Client
        fields=['company','address','job','mobile','profile_pic']
