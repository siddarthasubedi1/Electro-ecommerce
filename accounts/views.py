"""
Accounts Views
==============
This file handles user authentication and account management.

Key Functions:
- User registration
- User login (authentication)
- User logout
- Contact page

Django Authentication:
- authenticate(): Verify credentials (email + password)
- login(): Create session for user (remember they're logged in)
- logout(): End session (forget user)
- @login_required: Decorator to protect views (must be logged in)
"""

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# ============================================================
# USER REGISTRATION VIEW
# ============================================================
def register_view(request):
    """
    Handle user registration (sign up).

    URL: /accounts/register/
    Template: register.html
    Methods: GET (show form), POST (process form)

    Purpose:
        - Display registration form
        - Validate user input
        - Create new user account
        - Redirect to login page on success

    Logic Flow:
        1. If POST request (form submitted):
           - Validate form data
           - If valid, create user and redirect to login
           - If invalid, show errors
        2. If GET request (initial page load):
           - Show empty registration form
    """
    if request.method == "POST":
        # User submitted the registration form
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # Form data is valid, create the user
            form.save()  # Saves user to database

            # Show success message
            messages.success(
                request, "Account created successfully! Now you can login."
            )

            # Redirect to login page
            return redirect(reverse("accounts:loginpage"))
        # If form is invalid, it will show errors automatically
    else:
        # GET request - show empty form
        form = CustomUserCreationForm()

    context = {
        "form": form,  # Pass form to template
    }
    return render(request, "register.html", context)


# ============================================================
# USER LOGIN VIEW
# ============================================================
def login_view(request):
    """
    Handle user login (authentication).

    URL: /accounts/login/
    Template: login.html
    Methods: GET (show form), POST (process login)

    Purpose:
        - Display login form
        - Verify user credentials (email + password)
        - Create session (remember user is logged in)
        - Handle "Remember Me" functionality

    Features:
        - Email is automatically converted to lowercase
        - Remember Me checkbox controls session duration
        - Shows error messages for invalid credentials

    Logic Flow:
        1. If POST request (login attempt):
           - Get email and password from form
           - Authenticate credentials
           - If valid, log user in and redirect to homepage
           - If invalid, show error message
        2. If GET request (initial page load):
           - Show login form
    """
    # Optional: Uncomment to redirect already logged-in users
    # if request.user.is_authenticated:
    #     return redirect(reverse('store:homepage'))

    if request.method == "POST":
        # Get form data
        # .strip() removes whitespace, .lower() converts to lowercase
        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password")
        remember_me = request.POST.get("remember")  # Checkbox value

        # Verify credentials - returns User object if valid, None if invalid
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Credentials are valid - log user in
            # This creates a session and sets session cookies
            login(request, user)

            # Handle "Remember Me" functionality
            if not remember_me:
                # If "Remember Me" is NOT checked:
                # Session expires when browser closes
                request.session.set_expiry(0)
            # If checked: Session uses default expiration (2 weeks)

            # Show success message
            messages.success(request, "Logged in successful")

            # Redirect to homepage
            return redirect(reverse("store:homepage"))
        else:
            # Invalid credentials - show error
            messages.error(request, "Email or Password is invalid")

    # GET request or failed login - show login form
    return render(request, "login.html")


# ============================================================
# USER LOGOUT VIEW
# ============================================================
def logout_view(request):
    """
    Handle user logout.

    URL: /accounts/logout/

    Purpose:
        - End user session (forget they're logged in)
        - Clear session data
        - Redirect to login page

    Note:
        - Can be called from any page
        - Usually triggered by clicking "Logout" button
    """
    # End the session (log user out)
    logout(request)

    # Redirect to login page
    return redirect(reverse("accounts:loginpage"))


# ============================================================
# PROTECTED HOME VIEW (EXAMPLE)
# ============================================================
@login_required  # User must be logged in to access this view
def home_view(request):
    """
    Example of a login-protected view.

    Decorator @login_required:
        - If user is not logged in, redirects to LOGIN_URL (settings.py)
        - If user is logged in, allows access to view

    Note: This view currently just redirects to base.html
          Consider removing if not used.
    """
    return redirect(reverse("base.html"))


# ============================================================
# CONTACT PAGE VIEW
# ============================================================
def contact_view(request):
    """
    Display contact page.

    URL: /accounts/contact/
    Template: contact.html

    Purpose:
        - Show contact information
        - Display contact form (if implemented)

    Note:
        - Currently just renders template
        - Could be enhanced to handle contact form submissions
    """
    return render(request, "contact.html")
