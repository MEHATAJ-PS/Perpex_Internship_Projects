from django.urls import path
from .views import *
from .menu_views import SimpleMenuView 

urlpatterns = [
    path('items/', ItemView.as_view(), name='item-list'),
    path('menu/', MenuAPIView.as_view(), name='menu-list'),
    path('simple-menu/', SimpleMenuView.as_view(), name='simple_menu'),
]