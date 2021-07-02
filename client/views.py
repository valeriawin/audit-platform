from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from docs import forms as bforms
from docs import models as bmodels


def client_signup_view(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.user=user
            client.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        return HttpResponseRedirect('clientlogin')
    return render(request,'client/clientsignup.html',context=mydict)

def client_dashboard_view(request):
    client= models.Client.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.DocsRequest.objects.all().filter(request_by_client=client).filter(status='Pending').count(),
        'requestapproved': bmodels.DocsRequest.objects.all().filter(request_by_client=client).filter(status='Approved').count(),
        'requestmade': bmodels.DocsRequest.objects.all().filter(request_by_client=client).count(),
        'requestrejected': bmodels.DocsRequest.objects.all().filter(request_by_client=client).filter(status='Rejected').count(),

    }
   
    return render(request,'client/client_dashboard.html',context=dict)

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            docs_request=request_form.save(commit=False)
            docs_request.docsgroup=request_form.cleaned_data['docsgroup']
            client= models.Client.objects.get(user_id=request.user.id)
            docs_request.request_by_client=client
            docs_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'client/makerequest.html',{'request_form':request_form})

def my_request_view(request):
    client= models.Client.objects.get(user_id=request.user.id)
    docs_request=bmodels.DocsRequest.objects.all().filter(request_by_client=client)
    return render(request,'client/my_request.html',{'docs_request':docs_request})
