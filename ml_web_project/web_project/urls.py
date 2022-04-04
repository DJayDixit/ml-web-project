from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="project-home"),
    path('about/', views.about, name="project-about"),
    path('contact/', views.contact, name="project-contact"),
]

