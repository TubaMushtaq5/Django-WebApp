from django.urls import path
from .views import signup_view, login_view, profile_edit_view, logout_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/edit/', profile_edit_view, name='profile_edit'),
]
