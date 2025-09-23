from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    # New field for opening days
    opening_days = models.CharField(
        max_length=100,
        help_text="Comma-separated list of operating days (e.g., Mon,Tue,Wed,Thu,Fri,Sat,Sun)"
    )

    def __str__(self):
        return self.name
