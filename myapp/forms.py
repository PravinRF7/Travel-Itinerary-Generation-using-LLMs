from django import forms
from .models import Profile
from .models import Contact   

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo']
        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'file-upload',  # Apply custom class for CSS
            }),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

