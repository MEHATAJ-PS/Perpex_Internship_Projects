import requests
from django.shortcuts import render, redirect
from .models import RestaurantInfo, Feedback
from django.conf import settings
from django.utils import timezone
from django.contrib import messages

def menu_view(request):
    """
    Fetch menu items from the products API and render the menu page.
    """
    
    api_url = 'http://127.0.0.1:8000/api/products/menu/'

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        menu_items = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to fetch menu items: {e}")
        menu_items = []

    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant" 
    
    return render(request, 'home/menu.html', {
        'menu': menu_items,
        'restaurant_name': restaurant_name
    })


def custom_404_view(request, exception):
    """
    custom 404 page with restaurant name.
    """
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"
    
    return render(request, 'home/404.html', {
        'restaurant_name': restaurant_name
    }, status=404)

def homepage(request):
    """
    Render the homepage with basic restaurant info.
    """
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"
    phone_number = getattr(settings, "RESTAURANT_PHONE_NUMBER", "N/A")

    return render(request, 'home/index.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number,
    })

def about_view(request):
    """
    Render the About Us page with restaurant name.
    """
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"
    return render(request, 'home/about.html', {'restaurant_name': restaurant_name})

def contact_view(request):
    """
    Render the Contact Us page with hardcoded contact info.
    """
    contact_info = {
        "phone": "+1 (555) 123-4567",
        "email": "info@myrestaurant.com",
        "address": "123 Food Street, Flavor Town, USA",
        "hours": "Mon-Sat: 10am - 10pm, Sun: Closed"
    }

    
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"

    return render(request, "home/contact.html", {
        "contact": contact_info,
        "restaurant_name": restaurant_name,
    })

def reservations_view(request):
    """
    Render Reservations page with contact details and current time.
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

def feedback_view(request):
    """
    Handle feedback form submission and display.
    """
    restaurant_info = RestaurantInfo.objects.first()
    restaurant_name = restaurant_info.name if restaurant_info else "My Restaurant"

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message= request.POST.get("message", "").strip()

        if name and email and message:
            Feedback.objects.create(name=name, email=email, message=message)
            messages.success(request, "Thank you! Your feedback has been submitted.")
            return redirect("feedback") # Redirect to avoid form resubmission
        else:
            messages.error(request, "All fields are required.")
    
    feedback_list = Feedback.objects.all().order_by('-created_at')

    return render(request, "home/feedback.html", {
        "restaurant_name": restaurant_name,
        "feedback_list": feedback_list
    })