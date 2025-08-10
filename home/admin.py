from django.contrib import admin
from .models import RestaurantInfo

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    """
    Admin configuration for RestaurantInfo model.
    """
    list_display = ('name',) # Columns shown in admin list view
    search_fields = ('name',) # Search bar for restaurant names
