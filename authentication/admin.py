from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Fields to display in admin list view
    list_display = ('username', 'email', 'phone_number', 'profile_pic', 'is_staff', 'is_active')
    # Fields to use for search
    search_fields = ('username', 'email', 'phone_number')
    # Fieldsets for the admin detail page
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'profile_pic', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'profile_pic', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
