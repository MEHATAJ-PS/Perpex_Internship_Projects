from django.contrib import admin
from .models import RestaurantInfo, Feedback

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    """
    Admin configuration for RestaurantInfo model.
    """
    list_display = ('name',) # Columns shown in admin list view
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
