import requests
from django.shortcuts import render
from .models import RestaurantInfo

def menu_view(request):
    
    api_url = 'http://127.0.0.1:8000/api/products/menu/'

    try:
        response = requests.get(api_url)
        menu_items = response.json()
    except requests.exceptions.RequestException:
        menu_items = [] 
    
    return render(request, 'home/menu.html', {'menu': menu_items})



def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)

def homepage(request):
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"

    return render(request, 'home/index.html', {'restaurant_name': restaurant_name})

def about_view(request):
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"
    return render(request, 'home/about.html', {'restaurant_name': restaurant_name})