from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Client/',null=True,blank=True)
    company=models.CharField(max_length=100)
    job=models.CharField(max_length=50)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name