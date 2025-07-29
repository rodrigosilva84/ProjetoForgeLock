from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('verify-sms/', views.verify_sms, name='verify_sms'),
    path('resend-sms/', views.resend_sms, name='resend_sms'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('company-setup/', views.company_setup, name='company_setup'),
    path('change-language/', views.change_language, name='change_language'),
    path('api/country/<int:country_id>/ddi/', views.get_country_ddi, name='get_country_ddi'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]