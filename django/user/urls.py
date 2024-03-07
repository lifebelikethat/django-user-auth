from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('register/', views.RegisterPage, name='register'),
    path('confirm/', views.ResendConfirmEmail, name='resend-confirm'),
    path('confirm/<str:token>/', views.ConfirmEmail, name='confirm'),
    path('change-password/', views.ChangePassword, name='change-password'),
    path('reset-password/', views.ResetPasswordEmail, name='reset-password-email'),
    path('reset-password/<str:token>/', views.ResetPassword, name='reset-password'),
    path('change-email/', views.ChangeEmail, name='change-email'),
    path('change-email/<str:token>/', views.ChangeEmailConfirm, name='change-email-confirm'),
    ]
