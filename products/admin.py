from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for Item model.
    Provides search, filtering, and ordering functionality for menu items.
    """
    list_display = ['item_name', 'item_price', 'created_at']
    search_fields = ['item_name', 'description']
    list_filter = ['created_at']
    ordering = ['item_name']

    
admin.site.register(Item, ItemAdmin)