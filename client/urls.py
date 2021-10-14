from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('clientlogin', LoginView.as_view(template_name='client/clientlogin.html'),name='clientlogin'),
    path('clientsignup', views.client_signup_view,name='clientsignup'),
    
    path('client-dashboard', views.client_dashboard_view,name='client-dashboard'),
    
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
]
