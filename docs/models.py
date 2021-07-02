from django.db import models
from client import models as pmodels
from auditor import models as dmodels
import os

class Stock(models.Model):
    docsgroup=models.CharField(max_length=20)
    unit=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.docsgroup

class DocsRequest(models.Model):
    request_by_client=models.ForeignKey(pmodels.Client,null=True,on_delete=models.CASCADE)
    request_by_auditor=models.ForeignKey(dmodels.Auditor,null=True,on_delete=models.CASCADE)
    client_id=models.CharField(max_length=30)
    client_num=models.PositiveIntegerField()
    reason=models.CharField(max_length=500)
    docsgroup=models.CharField(max_length=20)
    audit_file= models.CharField(max_length=500)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)

    @property
    def filename(self):
        return os.path.basename(self.audit_file.name)

    def __str__(self):
        return self.docsgroup

        