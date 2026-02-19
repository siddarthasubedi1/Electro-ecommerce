"""
Accounts Admin Configuration
=============================
This file registers the CustomUser model with Django's admin interface.

Django Admin:
- Provides web interface to manage users
- Access at http://localhost:8000/admin/
- Only superusers can access

Purpose:
- View/edit/delete user accounts
- See user details (email, name, join date, etc.)
- Manage user permissions and groups
"""

from django.contrib import admin
from .models import CustomUser

# ============================================================
# REGISTER CUSTOM USER MODEL
# ============================================================
# Register CustomUser so it appears in admin panel
# Allows admin to manage all registered users
admin.site.register(CustomUser)

# Note: For more advanced admin features, you can create a UserAdmin class:
# from django.contrib.auth.admin import UserAdmin
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['email', 'first_name', 'last_name', 'is_staff']
#     list_filter = ['is_staff', 'is_superuser', 'is_active']
#     search_fields = ['email', 'first_name', 'last_name']
#     ordering = ['email']
# admin.site.register(CustomUser, CustomUserAdmin)
