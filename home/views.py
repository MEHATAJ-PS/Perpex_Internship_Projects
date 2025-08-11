import requests
from django.shortcuts import render
from .models import RestaurantInfo
from django.conf import settings
from django.utils import timezone

def menu_view(request):
    
    api_url = 'http://127.0.0.1:8000/api/products/menu/'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        menu_items = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching menu items: {e}")
        menu_items = [] 
    
    return render(request, 'home/menu.html', {'menu': menu_items})



def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)

def homepage(request):
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"
    phone_number = getattr(settings, "RESTAURANT_PHONE_NUMBER", "N/A")

    return render(request, 'home/index.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number,
    })

def about_view(request):
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"
    return render(request, 'home/about.html', {'restaurant_name': restaurant_name})

def contact_view(request):
    """
    Render a simple Contact Us page with hardcoded info.
    """
    contact_info = {
        "phone": "+1 (555) 123-4567",
        "email": "info@myrestaurant.com",
        "address": "123 Food Street, Flavor Town, USA",
        "hours": "Mon-Sat: 10am - 10pm, Sun: Closed"
    }

    restaurant_info = None
    try:
        from .models import RestaurantInfo
        restaurant_info = RestaurantInfo.objects.first()
    except ImportError:
        pass

    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"

    return render(request, "home/contact.html", {
        "contact": contact_info,
        "restaurant_name": restaurant_name,
    })

def reservations_view(request):
    """
    Render Reservations placeholder page.
    """
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"
    phone_number = getattr(settings, "RESTAURANT_PHONE_NUMBER", "N/A")
    contact_email = getattr(settings, "RESTAURANT_CONTACT_EMAIL", None)

    return render(request, 'home/reservations.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number,
        'contact_email': contact_email,
        'now': timezone.now(),
    })