from django import forms
from .models import Feedback


class feedbackForm(forms.ModelForm):
    """
    Form for users to submit feedback.
    """
    class meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Feedback', 'rows': 5}),
        }