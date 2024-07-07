"""
URL configuration for sam_sir_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('djadmin/', admin.site.urls),
    path('login/', views.LoginPage, name = 'login'),
    path('', views.SignupPage, name = 'signup'),
    path('home/', views.HomePage, name = 'home'),
    path('logout/', views.LogoutPage, name = 'logout'),
    path('form1/', views.FormPage_1, name = 'form1'),
    path('form2/', views.FormPage_2, name = 'form2'),
    path('forms/', views.UserChoice, name = 'choice'),
    path('reports/', views.ReportChoice, name = 'adminreport'),
    path('report1/', views.DailyAudio, name = 'dailyreport1'),
    path('report2/', views.DailySession, name = 'dailyreport2'),
    path('batches/', views.BatchChoice, name = 'batchchoice')



]

