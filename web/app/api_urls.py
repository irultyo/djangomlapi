from django.urls import path
from . import api

urlpatterns = [
    path('home', api.HomeView.as_view(), name='home'),
    path('retrieve', api.RetrieveView.as_view(), name='retrieve'),
    path('generate', api.GenerateView.as_view(), name='generate'),
]
