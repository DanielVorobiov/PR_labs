from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('receives.html', views.receives),
    path('message.html', views.message)
    #path('', views.index, name='index')
]
