from django import forms

class UserAlreadyExistsException(forms.ValidationError):
    def __init__(self, message="User with this email or username already exists"):
        super().__init__(message)

class InvalidPhoneNumberException(forms.ValidationError):
    def __init__(self, message="The phone number provided is invalid"):
        super().__init__(message)