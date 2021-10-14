from django import forms
from . import models


class DocsForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['docsgroup','unit']

        
class RequestForm(forms.ModelForm):
    class Meta:
        model=models.DocsRequest
        fields=['client_id','client_num','reason','docsgroup','audit_file']
