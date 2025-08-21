import requests
from django.shortcuts import render, redirect
from .models import RestaurantInfo, Feedback, ContactSubmission
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from .forms import FeedbackForm, ContactSubmissionForm


def get_restaurant_info():
    """Helper to get restaurant info or defaults."""
    restaurant = RestaurantInfo.objects.first()
    return {
        "name": getattr(restaurant, "name", "My restaurant"),
        "phone": getattr(restaurant, "phone_number", "+91 98765 43210"),
        "address": getattr(restaurant, "address", "Address not available"),
    }

def menu_view(request):
    """Fetch menu items from the products API and render the menu page.""" 
    api_url = 'http://127.0.0.1:8000/api/products/menu/'

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        menu_items = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to fetch menu items: {e}")
        menu_items = []

    # Search filter
    query = request.GET.get("q", "").strip()
    if isinstance(menu_items, list) and query:
        menu_items = [
            item for item in menu_items 
            if query.lower() in item("name", "").lower()
        ]

    info = get_restaurant_info()
    return render(request, 'home/menu.html', {
        'menu': menu_items,
        'restaurant_name': info.get("name", "Restaurant"),
        'search_query': query
    })


def custom_404_view(request, exception):
    """custom 404 page with restaurant name."""
    info = get_restaurant_info()
    return render(request, 'home/404.html', {
        'restaurant_name': info["name"]
    }, status=404)

def homepage(request):
    """Render the homepage with basic restaurant info and address from DB."""
    info = get_restaurant_info()
    contact_info = {
        "phone": info["phone"],
        "email": getattr(settings, "RESTAURANT_CONTACT_EMAIL", "info@delishrestaurant.com"),
        "address": info["address"],
        "hours": restaurant.opening_hours if restaurant else {}
    }
    return render(request, 'home/index.html', {
        'restaurant_name': info["name"],
        'phone_number': info["phone"],
        'contact_info': contact_info
    })

def about_view(request):
    """
    Render the About Us page with restaurant name.
    """
    info = get_restaurant_info()
    return render(request, 'home/about.html', {'restaurant_name': info["name"]})

def contact_view(request):
    """
    Render the Contact Us page with hardcoded contact info.
    """
    info = get_restaurant_info()
    if request.method == "POST":
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect("contact")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ContactSubmissionForm()


    contact_info = {
        "phone": info["phone"],
        "email": getattr(settings, "RESTAURANT_CONTACT_EMAIL", "info@delishrestaurant.com"),
        "address": info["address"],
        "hours": "Mon-Sun: 10am - 10pm",
    }

    
    return render(request, "home/contact.html", {
        "contact": contact_info,
        "restaurant_name": info["name"],
        "form": form
    })

def reservations_view(request):
    """
    Render Reservations page with contact details and current time.
    """
    info = get_restaurant_info()
    return render(request, 'home/reservations.html', {
        'restaurant_name': info["name"],
        'phone_number': getattr(settings, "RESTAURANT_PHONE_NUMBER", info["phone"]),
        'contact_email': getattr(settings, "RESTAURANT_CONTACT_EMAIL", "info@delishrestaurant.com"),
        'now': timezone.now(),
    })

def feedback_view(request):
    """
    Handle feedback form submission and display all feedbacks.
    """
    info = get_restaurant_info()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your feedback has been submitted.")
            return redirect("feedback") # Redirect to avoid form resubmission
        messages.error(request, "Please correct the errors below.")
    
    else:
        form = FeedbackForm()

    feedback_list = Feedback.objects.all().order_by('-submitted_at')
    return render(request, "home/feedback.html", {
        "restaurant_name": info["name"],
        "feedback_list": feedback_list,
        "form": form
    })