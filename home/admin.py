from django.contrib import admin
from .models import RestaurantInfo, Feedback, Contact, RestaurantLocation

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    """
    Admin configuration for RestaurantInfo model.
    """
    list_display = ('name', 'phone_number') # Columns shown in admin list view
    search_fields = ('name',) # Search bar for restaurant names


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin configuration for Feedback model.
    """
    list_display = ('name', 'email', 'comments', 'submitted_at') #Columns shown in list view
    search_fields = ('name', 'email', 'comments') # Enable search in admin
    list_filter = ('submitted_at',) # Sidebar filter for date
    ordering = ('-submitted_at',) # Most recent first


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for Contact model.
    """
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)


@admin.register(RestaurantLocation)
class RestaurantLocationAdmin(admin.ModelAdmin):
    """
    Admin configuration for RestaurantLocation model.
    """
    list_display = ('address', 'city', 'state', 'pincode')
    search_fields = ('address', 'city', 'state', 'pincode')
    list_filter = ('city', 'state')
    ordering = ('city',)