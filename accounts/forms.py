"""
Accounts Forms
==============
This file defines forms for user account management.

Form Types:
- UserCreationForm: Base class for creating new users
- CustomUserCreationForm: Extended version for our custom user model

Key Features:
- Email-based registration (not username)
- Password validation (length, complexity, etc.)
- First name and last name fields
- Bootstrap styling for all fields
"""

from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


# ============================================================
# CUSTOM USER REGISTRATION FORM
# ============================================================
class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new user accounts.

    Inherits from UserCreationForm which provides:
        - password1: Password field
        - password2: Password confirmation field
        - Built-in password validation

    Additional Fields:
        - email: User's email (used for login)
        - first_name: User's first name
        - last_name: User's last name

    All fields have Bootstrap CSS classes for styling.

    Validation:
        - Email must be unique (checked in model)
        - Password must meet Django's password requirements:
          * At least 8 characters
          * Not entirely numeric
          * Not too common
          * Not too similar to email/name
        - password1 and password2 must match
    """

    # ========== EMAIL FIELD ==========
    # EmailField: Validates email format (must contain @, valid domain, etc.)
    email = forms.EmailField(
        label="email",  # Label shown above field
        widget=forms.EmailInput(attrs={"class": "form-control"}),  # Bootstrap styling
        required=True,  # User must provide email
    )

    # ========== FIRST NAME FIELD ==========
    # CharField: Regular text input
    first_name = forms.CharField(
        label="first name",
        widget=forms.TextInput(attrs={"class": "form-control"}),  # Bootstrap styling
        required=True,  # User must provide first name
    )

    # ========== LAST NAME FIELD ==========
    # CharField: Regular text input
    last_name = forms.CharField(
        label="last name",
        widget=forms.TextInput(attrs={"class": "form-control"}),  # Bootstrap styling
        required=True,  # User must provide last name
    )

    # ========== PASSWORD FIELD (FIRST ENTRY) ==========
    # PasswordInput: Hides password characters (shows dots/asterisks)
    # Inherited from UserCreationForm but customized here
    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},  # Bootstrap styling
        ),
    )

    # ========== PASSWORD CONFIRMATION FIELD ==========
    # User must type password twice to confirm they didn't make typo
    # Form validation checks that password1 == password2
    password2 = forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},  # Bootstrap styling
        ),
    )

    class Meta:
        """
        Meta class defines additional form configuration.

        Attributes:
            - model: Which model this form creates (CustomUser)
            - fields: Which fields to include in form and their order

        Note: Fields are displayed in the order listed here.
        """

        model = CustomUser
        # Order: first name, last name, email, password, confirm password
        fields = ("first_name", "last_name", "email", "password1", "password2")
