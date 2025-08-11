from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('menu/', views.menu_view, name='menu'),
    path('about/', views.about_view, name='about'), 
    path('contact/', views.contact_view, name='contact'),
    path('reservations/', views.reservations_view, name='reservations'), 
]