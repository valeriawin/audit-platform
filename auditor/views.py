from django.shortcuts import render,redirect,reverse
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from docs import forms as dforms
from docs import models as dmodels

from . import forms,models
from datetime import date, timedelta


def auditor_signup_view(request):
    userForm=forms.AuditorUserForm()
    auditorForm=forms.AuditorForm()
    mydict={'userForm':userForm,'auditorForm':auditorForm}
    
    if request.method=='POST':
        userForm=forms.AuditorUserForm(request.POST)
        auditorForm=forms.AuditorForm(request.POST,request.FILES)
        auditorForm.job='стажер'
        
        if userForm.is_valid() and auditorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            auditor=auditorForm.save(commit=False)
            auditor.user=user
            auditor.save()
            my_auditor_group = Group.objects.get_or_create(name='AUDITOR')
            my_auditor_group[0].user_set.add(user)
            
        return HttpResponseRedirect('auditorlogin')
    
    return render(request,'auditor/auditorsignup.html',context=mydict)


def auditor_dashboard_view(request):
    dict={
        'requestpending': models.DocsAudit.objects.all().filter(status='Pending').count(),
        'requestapproved': models.DocsAudit.objects.all().filter(status='Approved').count(),
        'requestmade': models.DocsAudit.objects.all().count(),
        'requestrejected': models.DocsAudit.objects.all().filter(status='Rejected').count(),
    }
    
    return render(request,'auditor/auditor_dashboard.html',context=dict)


def auditor_request_view(request):
    requests=dmodels.DocsRequest.objects.all().filter(status='Pending')
    
    return render(request,'auditor/auditor_request.html',{'requests':requests})


def update_approve_status_view(request,pk):
    req=dmodels.DocsRequest.objects.get(id=pk)
    message=None
    docsgroup=req.docsgroup
    audit_file=req.audit_file
    
    stock=dmodels.Stock.objects.get(docsgroup=docsgroup)
    stock.unit+=1
    stock.save()
    req.status="Approved"
    req.save()
    requests=dmodels.DocsRequest.objects.all().filter(status='Pending')
    
    return render(request,'auditor/auditor_request.html',{'requests':requests,'message':message})


def update_reject_status_view(request,pk):
    req=dmodels.DocsRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    
    return HttpResponseRedirect('auditor/auditor-request')


def audit_docs_view(request):
    audition_form=forms.AuditionForm()
    
    if request.method=='POST':
        audition_form=forms.AuditionForm(request.POST)
        
        if audition_form.is_valid():
            docs_audit=audition_form.save(commit=False)
            docs_audit.docsgroup=audition_form.cleaned_data['docsgroup']
            auditor= models.Auditor.objects.get(user_id=request.user.id)
            docs_audit.auditor=auditor
            docs_audit.save()
            
            return HttpResponseRedirect('audition-history')  
        
    return render(request,'auditor/audit_docs.html',{'audition_form':audition_form})


def audition_history_view(request):
    auditor= models.Auditor.objects.get(user_id=request.user.id)
    auditions=models.DocsAudit.objects.all().filter(auditor=auditor)
    
    return render(request,'auditor/audition_history.html',{'auditions':auditions})


def make_request_view(request):
    request_form=dforms.RequestForm()
    
    if request.method=='POST':
        request_form=dforms.RequestForm(request.POST)
        
        if request_form.is_valid():
            docs_request=request_form.save(commit=False)
            docs_request.docsgroup=request_form.cleaned_data['docsgroup']
            auditor= models.Auditor.objects.get(user_id=request.user.id)
            docs_request.request_by_auditor=auditor
            docs_request.save()
            
            return HttpResponseRedirect('request-history') 
        
    return render(request,'auditor/makerequest.html',{'request_form':request_form})


def request_history_view(request):
    auditor= models.Auditor.objects.get(user_id=request.user.id)
    docs_request=dmodels.DocsRequest.objects.all().filter(request_by_auditor=auditor)
    
    return render(request,'auditor/request_history.html',{'docs_request':docs_request})
