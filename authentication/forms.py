from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .exceptions import UserAlreadyExistsException, InvalidPhoneNumberException

# class CustomUserCreationForm(UserCreationForm):
#     phone_number = forms.CharField(
#         max_length=15,
#         required=True,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Enter your phone number'
#         })
#     )
#     profile_pic = forms.ImageField(
#         required=True,  # make it mandatory
#         widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
#     )
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email", "phone_number","profile_pic", "password1", "password2")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'profile_pic']

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    profile_pic = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "profile_pic", "password1", "password2")

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit() or len(phone) < 10:
            raise InvalidPhoneNumberException(f"The phone number '{phone}' is invalid.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise UserAlreadyExistsException(f"A user with email '{email}' already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise UserAlreadyExistsException(f"A user with username '{username}' already exists.")
        return username