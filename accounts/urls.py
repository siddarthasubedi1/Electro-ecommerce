"""
Accounts URL Configuration
==========================
This file maps URLs to view functions for the accounts app.

Handles:
- User login
- User logout
- User registration
- Contact page

All URLs are prefixed with /accounts/ in the main urls.py
Example: /accounts/login/, /accounts/register/, etc.
"""

from django.urls import path
from . import views

# Namespace for these URLs - allows us to use {% url 'accounts:loginpage' %}
app_name = "accounts"

urlpatterns = [
    # ========== LOGIN PAGE ==========
    # URL: /accounts/login/
    # View: login_view() - handles user authentication
    # Name: 'loginpage' - use in templates as {% url 'accounts:loginpage' %}
    path("login/", views.login_view, name="loginpage"),
    # ========== LOGOUT ==========
    # URL: /accounts/logout/
    # View: logout_view() - ends user session
    # Name: 'logout'
    # Usually called when user clicks "Logout" button
    path("logout/", views.logout_view, name="logout"),
    # ========== REGISTRATION PAGE ==========
    # URL: /accounts/register/
    # View: register_view() - handles new user signup
    # Name: 'registerpage'
    path("register/", views.register_view, name="registerpage"),
    # ========== CONTACT PAGE ==========
    # URL: /accounts/contact/
    # View: contact_view() - displays contact information
    # Name: 'contactpage'
    path("contact/", views.contact_view, name="contactpage"),
]
