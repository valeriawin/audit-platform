from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView,LoginView
from docs import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auditor/',include('auditor.urls')),
    path('client/',include('client.urls')),

    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='docs/logout.html'),name='logout'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminlogin', LoginView.as_view(template_name='docs/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-docs', views.admin_docs_view,name='admin-docs'),
    path('admin-auditor', views.admin_auditor_view,name='admin-auditor'),
    path('admin-client', views.admin_client_view,name='admin-client'),
    path('admin-audition', views.admin_audition_view,name='admin-audition'),
    path('approve-audition/<int:pk>/<int:unit>', views.approve_audition_view,name='approve-audition'),
    path('admin-request-history', views.admin_request_history_view,name='admin-request-history'),
    
    path('update-auditor/<int:pk>', views.update_auditor_view,name='update-auditor'),
    path('delete-auditor/<int:pk>', views.delete_auditor_view,name='delete-auditor'),
    
    path('update-client/<int:pk>', views.update_client_view,name='update-client'),
    path('delete-client/<int:pk>', views.delete_client_view,name='delete-client'),
]
