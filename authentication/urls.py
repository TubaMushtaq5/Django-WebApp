from django.urls import path
from .views import SignupView,ProfileEditView,LoginView,LogoutView,HomeView,AddDateTimeView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile-edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add-datetime/', AddDateTimeView.as_view(), name='add_datetime'),
]