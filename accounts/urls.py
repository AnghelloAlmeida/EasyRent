# C:\easyrent_demo\accounts\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
]