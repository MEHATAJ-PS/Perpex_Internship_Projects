from django import forms
from .models import Feedback, Contact, ContactSubmission


class FeedbackForm(forms.ModelForm):
    """
    Form for users to submit feedback (name, email, and comments).
    Includes Bootstrap-friendly widgets and placeholders.
    """
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'comments']
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'comments': 'Your Feedback / Suggestions',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your email address'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your feedback or suggestions here...', 
                'rows': 5
            }),
        }
        help_texts = {
            'comments': 'Please be specific and constructive in your feedback.',
        }

class ContactForm(forms.ModelForm):
    """
    Basic Contact Us form with name and email.
    """
    class Meta:
        model = Contact
        fields = ['name', 'email']
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
        }


class ContactSubmissionForm(forms.ModelForm):
    """
    Form for task: Simple Contact Form Submission
    Allows user to submit name, email, and message.
    """
    class Meta:
        model = ContactSubmission
        fields =['name', 'email', 'message']
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'message': 'Your Message',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here...',
                'rows': 5
            }),
        }
        help_texts = {
            'name': 'Please enter your full name.',
            'email': 'we will contact you at this email address.',
            'message': 'Please describe your query or feedback clearly.',
        }


