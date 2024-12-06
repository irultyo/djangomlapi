from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('/', views.home, name='homepage'),
    path('/select_patch/', views.select_patch, name='select_patch'),
    path('/result/', views.result, name='result')
]
