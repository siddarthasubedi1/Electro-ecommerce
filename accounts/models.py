"""
Accounts Models
===============
This file defines custom user model and user manager for authentication.

Why Custom User Model?
- Django's default User model uses 'username' for login
- This project uses 'email' for login instead (more modern approach)
- Must create custom user model to change authentication field

Key Concepts:
- BaseUserManager: Handles creating users and superusers
- AbstractUser: Base class that provides all user functionality
- USERNAME_FIELD: Tells Django which field to use for login
"""

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# ============================================================
# CUSTOM USER MANAGER
# ============================================================
class CustomUserManager(BaseUserManager):
    """
    Custom manager for creating users with email instead of username.

    Purpose:
        - Override default create_user() and create_superuser() methods
        - Ensure email is required instead of username
        - Handle password hashing properly

    Methods:
        - create_user(): Create regular user
        - create_superuser(): Create admin user with all permissions
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a regular user with email and password.

        Parameters:
            - email: User's email address (used for login)
            - password: User's password (will be hashed)
            - **extra_fields: Additional fields (first_name, last_name, etc.)

        Returns:
            User object

        Raises:
            ValueError: If email is not provided
        """
        # Validate that email is provided
        if not email:
            raise ValueError(_("Email must be set."))

        # Normalize email (convert domain to lowercase, etc.)
        email = self.normalize_email(email)

        # Create user instance with email and extra fields
        user = self.model(email=email, **extra_fields)

        # Hash the password (NEVER store plain text passwords!)
        user.set_password(password)

        # Save to database
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser (admin) with email and password.

        Superuser has all permissions and can access Django admin panel.

        Parameters:
            - email: Admin's email address
            - password: Admin's password
            - **extra_fields: Additional fields

        Returns:
            User object with admin privileges

        Raises:
            ValueError: If is_staff or is_superuser is not True
        """
        # Set default values for superuser fields
        extra_fields.setdefault("is_staff", True)  # Can access admin panel
        extra_fields.setdefault("is_superuser", True)  # Has all permissions
        extra_fields.setdefault("is_active", True)  # Account is active

        # Validate that required fields are True
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff = True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser = True"))

        # Create user using create_user method
        return self.create_user(email, password, **extra_fields)


# ============================================================
# CUSTOM USER MODEL
# ============================================================
class CustomUser(AbstractUser):
    """
    Custom User model that uses email for authentication instead of username.

    Inherits from AbstractUser which provides:
        - password field
        - is_active, is_staff, is_superuser flags
        - first_name, last_name fields
        - date_joined, last_login timestamps
        - groups and permissions

    Changes from default Django User:
        - Removed: username field (set to None)
        - Changed: email is now unique and required
        - Changed: USERNAME_FIELD is email instead of username

    Fields:
        - email: EmailField, unique (used for login)
        - Inherits: password, first_name, last_name, is_active, etc.
    """

    # Remove username field (we don't need it)
    username = None

    # Email field - unique and required for login
    email = models.EmailField(
        _("Email Address"), unique=True  # No two users can have same email
    )

    # Tell Django to use email for login instead of username
    USERNAME_FIELD = "email"

    # EMAIL_FIELD is already set to "email" by default, so this is commented
    # EMAIL_FIELD = "email"

    # Required fields when creating superuser (besides email and password)
    # Empty list means only email and password are required
    REQUIRED_FIELDS = []

    # Use our custom manager instead of default
    objects = CustomUserManager()

    def __str__(self):
        """String representation of user (shown in admin and queries)"""
        return self.email

    def save(self, *args, **kwargs):
        """
        Override save method to normalize email to lowercase.

        Purpose:
            - Convert email to lowercase before saving
            - Prevents duplicates like "User@Email.com" and "user@email.com"
            - Ensures consistent email format

        Example:
            User enters: "John@Example.COM"
            Stored as: "john@example.com"
        """
        if self.email:
            self.email = self.email.lower()  # Convert to lowercase

        # Call parent save method to actually save to database
        super().save(*args, **kwargs)
