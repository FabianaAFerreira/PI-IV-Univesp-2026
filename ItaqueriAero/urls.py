from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name= "dashboard"),
    path("historico/", views.historico, name="historico"),
    
]