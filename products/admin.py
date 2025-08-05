from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name','item_price','created_at']


admin.site.register(Item,ItemAdmin)