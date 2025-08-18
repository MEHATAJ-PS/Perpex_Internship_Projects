from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Form for users to submit feedback (name, email, and comments).
    In
    """
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Feedback', 'rows': 5}),
        }