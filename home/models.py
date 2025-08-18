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
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Phone Number",
        help_text="Enter the restaurant's contact number."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurant Information"
        verbose_name_plural = "Restaurant Information"
        ordering = ['name']


class Contact(models.Model):
    """
    Stores Contact Us form submissions (basic).

    """
    name = models.CharField(
        max_length=100,
        verbose_name="Your Name",
        help_text="Enter your full name."
    )
    email = models.EmailField(
        verbose_name="Email Address",
        help_text="Enter your email address."
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Submitted At"
    )

    def __str__(self):
        return f"Contact from {self.name}"
    
    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ['-submitted_at']

class Feedback(models.Model):
    """
    Stores customer feedback submissions.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Your Name",
        help_text="Enter your full name."
    )
    email = models.EmailField(
        verbose_name="Email Address",
        help_text="Enter your email address."
    )
    comments = models.TextField(
        verbose_name="Comments",
        help_text="Enter your feedback or suggestions."
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Submitted At"
    )

    def __str__(self):
        return f"Feedback from {self.name}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
        ordering = ['-submitted_at']
