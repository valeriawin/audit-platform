from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('auditorlogin', LoginView.as_view(template_name='auditor/auditorlogin.html'),name='auditorlogin'),
    path('auditorsignup', views.auditor_signup_view,name='auditorsignup'),
    
    path('auditor-dashboard', views.auditor_dashboard_view,name='auditor-dashboard'),
    path('audit-docs', views.audit_docs_view,name='audit-docs'),
    path('audition-history', views.audition_history_view,name='audition-history'),
    
    path('make-request', views.make_request_view,name='make-request'),
    path('request-history', views.request_history_view,name='request-history'),
    path('auditor-request', views.auditor_request_view,name='auditor-request'),
    
    path('update-approve-status/<int:pk>', views.update_approve_status_view,name='update-approve-status'),
    path('update-reject-status/<int:pk>', views.update_reject_status_view,name='update-reject-status'),

]
