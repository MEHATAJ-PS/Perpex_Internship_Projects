import requests
from django.shortcuts import render, redirect
from .models import RestaurantInfo, Feedback, ContactSubmission
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from .forms import FeedbackForm, ContactSubmissionForm

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

    restaurant_name = getattr(RestaurantInfo.objects.first(), "name", "My Restaurant")
    
    return render(request, 'home/menu.html', {
        'menu': menu_items,
        'restaurant_name': restaurant_name
    })


def custom_404_view(request, exception):
    """
    custom 404 page with restaurant name.
    """
    restaurant_name = getattr(RestaurantInfo.objects.first(), "name", "My Restaurant")
    
    return render(request, 'home/404.html', {
        'restaurant_name': restaurant_name
    }, status=404)

def homepage(request):
    """
    Render the homepage with basic restaurant info.
    """

    restaurant_name = getattr(RestaurantInfo.objects.first(), "name", "My Restaurant")
    phone_number = getattr(settings, "RESTAURANT_PHONE_NUMBER", "+91 98765 43210")

    contact_info = {
        "phone": phone_number,
        "email": getattr(settings, "RESTAURANT_CONTACT_EMAIL", "info@delishrestaurant.com"),
        "address": "MG Road, Bangalore, India",
        "hours": "Mon-Sun: 10am - 10pm"
    }

    return render(request, 'home/index.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number,
        'contact_info': contact_info
    })

def about_view(request):
    """
    Render the About Us page with restaurant name.
    """
    restaurant_name = getattr(RestaurantInfo.objects.first(),"name", "My Restaurant")
    return render(request, 'home/about.html', {'restaurant_name': restaurant_name})

def contact_view(request):
    """
    Render the Contact Us page with hardcoded contact info.
    """
    restaurant_name = getattr(RestaurantInfo.objects.first(), "name", "My Restaurant")
    
    if request.method == "POST":
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect("contact")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactSubmissionForm()


    contact_info = {
        "phone": "+91 98765 43210",
        "email": "info@delishrestaurant.com",
        "address": "MG Road, Bangalore, India",
        "hours": "Mon-Sun: 10am - 10pm",
    }

    
    return render(request, "home/contact.html", {
        "contact": contact_info,
        "restaurant_name": restaurant_name,
        "form": form
    })

def reservations_view(request):
    """
    Render Reservations page with contact details and current time.
    """
    restaurant_name = getattr(RestaurantInfo.objects.first(), "name", "My Restaurant")
    phone_number = getattr(settings, "RESTAURANT_PHONE_NUMBER", "+91 98765 43210")
    contact_email = getattr(settings, "RESTAURANT_CONTACT_EMAIL", "info@delishrestaurant.com")

    return render(request, 'home/reservations.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number,
        'contact_email': contact_email,
        'now': timezone.now(),
    })

def feedback_view(request):
    """
    Handle feedback form submission and display all feedbacks.
    """
    restaurant_name = getattr(RestaurantInfo.objects.first(), "name", "My Restaurant")

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your feedback has been submitted.")
            return redirect("feedback") # Redirect to avoid form resubmission
        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        form = FeedbackForm()

    feedback_list = Feedback.objects.all().order_by('-submitted_at')

    return render(request, "home/feedback.html", {
        "restaurant_name": restaurant_name,
        "feedback_list": feedback_list,
        "form": form
    })