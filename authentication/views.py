from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from authentication.models import CustomUser
from .forms import CustomUserCreationForm, ProfileEditForm
from .exceptions import UserAlreadyExistsException, InvalidPhoneNumberException
from django.core.exceptions import ValidationError
from .exceptions import UserAlreadyExistsException, InvalidPhoneNumberException

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        # no need to manually catch anything — form.errors handles it
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/signup.html', {'form': form})

# def signup_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)

#         try:
#             if form.is_valid():
#                 username = form.cleaned_data['username']
#                 email = form.cleaned_data['email']
#                 phone = form.cleaned_data['phone_number']

#                 if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
#                     print("User with this username or email already existssssss.")
#                     raise UserAlreadyExistsException(f"A user with username '{username}' or email '{email}' already exists.")

#                 if not phone.isdigit() or len(phone) < 10:
#                     raise InvalidPhoneNumberException(f"The phone number '{phone}' is invalid.")

#                 user = form.save()
#                 login(request, user)
#                 return redirect('home')

#             # else:
#             #     messages.error(request, "Please correct the errors below.")

#         except UserAlreadyExistsException as e:
#             messages.error(request, str(e))
#         except InvalidPhoneNumberException as e:
#             messages.error(request, str(e))

#     else:
#         form = CustomUserCreationForm()

#     return render(request, 'authentication/signup.html', {'form': form})

# def signup_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'authentication/signup.html', {'form': form})

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'authentication/profile_edit.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/auth/login/')
def home_view(request):
    return render(request, 'home.html')