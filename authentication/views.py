from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pytz

from authentication.models import CustomUser, PSTDateTimeRecord
from .forms import CustomUserCreationForm, ProfileEditForm


def signup_view(request):
    if request.method == 'POST':
        # ModelForm as CustomUserCreationForm
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/signup.html', {'form': form})

# @login_required
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
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate using email
        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'authentication/login.html')
# @login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='/auth/login/')
def home_view(request):
    records = PSTDateTimeRecord.objects.filter(user=request.user).order_by('-datetime_pst')
    return render(request, "home.html", {"records": records})

# @login_required(login_url='/auth/login/')
def add_datetime(request):
    print(f"Logged-in user: {request.user.username}")
    if request.method == "POST":
        title = request.POST.get("title")
        region = request.POST.get("region")
        print(f"Received title: {title}, region: {region}")
        if title and region:
            now_utc = timezone.now()
            pst_tz = pytz.timezone("America/Los_Angeles")
            print(f"Current UTC time: {now_utc}")
            if region == "utc":
                aware_dt = now_utc.astimezone(pst_tz)
            else:
                aware_dt = now_utc.astimezone(pst_tz)
            # Save record
            
            PSTDateTimeRecord.objects.create(title=title, datetime_pst=aware_dt,user=request.user)
            print(f"Data to be added: {aware_dt}")
            
    return redirect("home")
    # Fetch all records for display
    # records = PSTDateTimeRecord.objects.filter(user=request.user)
    # return render(request, "home.html", {"records": records})