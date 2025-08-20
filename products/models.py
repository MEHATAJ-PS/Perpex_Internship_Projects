from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=150)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, help_text="Description of the menu item")
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Direct link to the item image"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item_name)


    class Meta:
        ordering = ['item_name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'