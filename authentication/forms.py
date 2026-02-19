from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number'
        })
    )
    profile_pic = forms.ImageField(
        required=True,  # make it mandatory
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'profile_pic']
