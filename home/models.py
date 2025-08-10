from django.db import models

class RestaurantInfo(models.Model):
    """
    Stores basic restaurant information.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Restaurant Name",
        help_text="Enter the name of the restaurant."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurant Information"
        verbose_name_plural = "Restaurant Information"
        ordering = ['name']
