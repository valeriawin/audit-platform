from django.shortcuts import render,redirect,reverse
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from auditor import models as dmodels
from client import models as pmodels
from auditor import forms as dforms
from client import forms as pforms
from . import forms,models

from datetime import date, timedelta


def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    
    if len(x)==0:
        docs1=models.Stock()
        docs1.docsgroup="Финансовый"
        docs1.save()

        docs2=models.Stock()
        docs2.docsgroup="Управленческий"
        docs2.save()

        docs3=models.Stock()
        docs3.docsgroup="Хоз. деятельности"
        docs3.save()        

        docs4=models.Stock()
        docs4.docsgroup="Специальный"
        docs4.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    
    return render(request,'docs/index.html')


def is_auditor(user):
    return user.groups.filter(name='AUDITOR').exists()


def is_client(user):
    return user.groups.filter(name='CLIENT').exists()


def afterlogin_view(request):
    if is_auditor(request.user):      
        return redirect('auditor/auditor-dashboard')
    elif is_client(request.user):
        return redirect('client/client-dashboard')
    else:
        return redirect('admin-dashboard')

    
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit=models.Stock.objects.aggregate(Sum('unit'))
    dict={
        'D1':models.Stock.objects.get(docsgroup="Финансовый"),
        'D2':models.Stock.objects.get(docsgroup="Управленческий"),
        'D3':models.Stock.objects.get(docsgroup="Хоз. деятельности"),
        'D4':models.Stock.objects.get(docsgroup="Специальный"),
        'totalauditors':dmodels.Auditor.objects.all().count(),
        'totaldocsunit':(totalunit['unit__sum']),
        'totalrequest':models.DocsRequest.objects.all().count(),
        'totalapprovedrequest':models.DocsRequest.objects.all().filter(status='Approved').count()
    }
    
    return render(request,'docs/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_docs_view(request):
    dict={
        'docsForm':forms.DocsForm(),
        'D1':models.Stock.objects.get(docsgroup="Финансовый"),
        'D2':models.Stock.objects.get(docsgroup="Управленческий"),
        'D3':models.Stock.objects.get(docsgroup="Хоз. деятельности"),
        'D4':models.Stock.objects.get(docsgroup="Специальный"),
    }
    
    if request.method=='POST':
        docsForm=forms.DocsForm(request.POST)
        if docsForm.is_valid() :        
            docsgroup=docsForm.cleaned_data['docsgroup']
            stock=models.Stock.objects.get(docsgroup=docsgroup)
            stock.unit=docsForm.cleaned_data['unit']
            stock.save()
            
        return HttpResponseRedirect('admin-docs')
    
    return render(request,'docs/admin_docs.html',context=dict)


@login_required(login_url='adminlogin')
def admin_auditor_view(request):
    auditors=dmodels.Auditor.objects.all()
    
    return render(request,'docs/admin_auditor.html',{'auditors':auditors})


@login_required(login_url='adminlogin')
def update_auditor_view(request,pk):
    auditor=dmodels.Auditor.objects.get(id=pk)
    user=dmodels.User.objects.get(id=auditor.user_id)
    userForm=dforms.AuditorUserForm(instance=user)
    auditorForm=dforms.AuditorForm(request.FILES,instance=auditor)
    mydict={'userForm':userForm,'auditorForm':auditorForm}
    
    if request.method=='POST':
        userForm=dforms.AuditorUserForm(request.POST,instance=user)
        auditorForm=dforms.AuditorForm(request.POST,request.FILES,instance=auditor)
        
        if userForm.is_valid() and auditorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            auditor=auditorForm.save(commit=False)
            auditor.user=user
            auditor.save()
            
            return redirect('admin-auditor')
        
    return render(request,'docs/update_auditor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_auditor_view(request,pk):
    auditor=dmodels.Auditor.objects.get(id=pk)
    user=User.objects.get(id=auditor.user_id)
    user.delete()
    auditor.delete()
    
    return HttpResponseRedirect('/admin-auditor')


@login_required(login_url='adminlogin')
def admin_client_view(request):
    clients=pmodels.Client.objects.all()
    
    return render(request,'docs/admin_client.html',{'clients':clients})


@login_required(login_url='adminlogin')
def update_client_view(request,pk):
    client=pmodels.Client.objects.get(id=pk)
    user=pmodels.User.objects.get(id=client.user_id)
    userForm=pforms.ClientUserForm(instance=user)
    clientForm=pforms.ClientForm(request.FILES,instance=client)
    mydict={'userForm':userForm,'clientForm':clientForm}
    
    if request.method=='POST':
        userForm=pforms.ClientUserForm(request.POST,instance=user)
        clientForm=pforms.ClientForm(request.POST,request.FILES,instance=client)
        
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.user=user
            client.save()
            
            return redirect('admin-client')
        
    return render(request,'docs/update_client.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_client_view(request,pk):
    client=pmodels.Client.objects.get(id=pk)
    user=User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    
    return HttpResponseRedirect('/admin-client')


@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=models.DocsRequest.objects.all().exclude(status='Pending')
    
    return render(request,'docs/admin_request_history.html',{'requests':requests})


@login_required(login_url='adminlogin')
def admin_audition_view(request):
    auditions=dmodels.DocsAudit.objects.all()
    
    return render(request,'docs/admin_audition.html',{'auditions':auditions})


@login_required(login_url='adminlogin')
def approve_audition_view(request,pk, unit):
    audition=dmodels.DocsAudit.objects.get(id=pk)
    worker=dmodels.Auditor.objects.get(id=audition.auditor_id)
    
    if unit>=audition.unit:
        audition.status='Approved'
    else:
        audition.status='Rejected'

    if worker.job == 'стажер':
        audition.unit=audition.unit*0.09+unit*0.91
    elif worker.job == 'аудитор':
        audition.unit=audition.unit*0.3+unit*0.7
    elif worker.job == 'главный аудитор':
        audition.unit=audition.unit*0.5+unit*0.5
        
    audition.save()
    
    audition_f=dmodels.DocsAudit.objects.all()
    f1 = open('unit', 'w')
    str_audition = ""
    
    for elem in audition_f:
        str_audition = str_audition + str(elem.unit) + " "
        
    f1.write(str_audition)
    f1.close()

    stock=models.Stock.objects.get(docsgroup=audition.docsgroup)
    stock.unit=stock.unit+1
    stock.save()    

    stock_f=models.Stock.objects.all()
    f2 = open('stock', 'w')
    str_stock = ""
    
    for elem in stock_f:
        str_stock = str_stock + str(elem.unit) + " "
        
    f2.write(str_stock)
    f2.close()
    
    return HttpResponseRedirect('/admin-audition')
