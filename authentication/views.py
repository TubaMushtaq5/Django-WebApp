
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import pytz

from authentication.models import CustomUser, PSTDateTimeRecord
from .forms import CustomUserCreationForm, ProfileEditForm

# ===========================
# Signup View
# ===========================
class SignupView(View):
    template_name = 'authentication/signup.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

# ===========================
# Profile Edit View
# ===========================
class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'authentication/profile_edit.html'
    login_url = '/auth/login/'

    def get(self, request):
        form = ProfileEditForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


# ===========================
# Login View
# ===========================
class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
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
            return render(request, self.template_name)

# ===========================
# Logout View
# ===========================
class LogoutView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def post(self, request):
        logout(request)
        return redirect('login')


# ===========================
# Home View
# ===========================
class HomeView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        records = PSTDateTimeRecord.objects.filter(user=request.user).order_by('-datetime_pst')
        return render(request, "home.html", {"records": records})


# ===========================
# Add DateTime View
# ===========================
class AddDateTimeView(LoginRequiredMixin, View):

    def post(self, request):
        title = request.POST.get("title")
        region = request.POST.get("region")

        if title and region:
            now_utc = timezone.now()
            pst_tz = pytz.timezone("America/Los_Angeles")

            # You can adjust here if you want UTC conversion
            aware_dt = now_utc.astimezone(pst_tz)

            # Save record
            PSTDateTimeRecord.objects.create(
                title=title,
                datetime_pst=aware_dt,
                user=request.user
            )

        return redirect("home")