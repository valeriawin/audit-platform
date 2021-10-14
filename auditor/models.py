from django.db import models
from django.contrib.auth.models import User


class Auditor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Auditor/',null=True,blank=True)
    mobile = models.CharField(max_length=20,null=False)
    job = models.CharField(max_length=20,null=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_instance(self):
        return self
    
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

    
class DocsAudit(models.Model): 
    auditor=models.ForeignKey(Auditor,on_delete=models.CASCADE)   
    info=models.CharField(max_length=100,default="Nothing")
    id_doc=models.PositiveIntegerField()
    docsgroup=models.CharField(max_length=20)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.auditor
    
