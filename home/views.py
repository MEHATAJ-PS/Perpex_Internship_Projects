import requests
from django.shortcuts import render

def menu_view(request):
    
    api_url = 'http://127.0.0.1:8000/api/products/menu/'

    try:
        response = requests.get(api_url)
        menu_items = response.json()
    except requests.exceptions.RequestException:
        menu_items = [] 
    
    return render(request, 'home/menu.html', {'menu': menu_items})

