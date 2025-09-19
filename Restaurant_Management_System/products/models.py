from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=150)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, help_text="Description of the menu item")
    image = models.ImageField(
        upload_to='menu_images',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item_name)


    class Meta:
        ordering = ['item_name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'