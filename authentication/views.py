from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileEditForm


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

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