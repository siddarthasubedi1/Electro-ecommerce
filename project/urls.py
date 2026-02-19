from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ============================================================
# URL PATTERNS
# ============================================================
urlpatterns = [
    # ========== ADMIN PANEL ==========
    # URL: /admin/
    # Django's built-in admin interface for managing database
    # Only accessible by superusers (created with: python manage.py createsuperuser)
    # Access at: http://localhost:8000/admin/
    path("admin/", admin.site.urls),
    # ========== ACCOUNTS APP URLS ==========
    # URL prefix: /accounts/
    # All URLs from accounts/urls.py will be prefixed with /accounts/
    # Examples:
    #   /accounts/login/    -> login page
    #   /accounts/register/ -> registration page
    #   /accounts/logout/   -> logout action
    #   /accounts/contact/  -> contact page
    path("accounts/", include("accounts.urls")),
    # ========== STORE APP URLS (ROOT) ==========
    # URL prefix: / (root)
    # All URLs from store/urls.py are at root level
    # include(("store.urls", "store"), namespace="store"):
    #   - First argument: ("store.urls", "store") - module and app name
    #   - namespace="store": Allows using {% url 'store:homepage' %} in templates
    # Examples:
    #   /              -> homepage
    #   /shop/         -> product listing page
    #   /product/5/detail/ -> product detail page
    #   /cart/5/add    -> add product to cart
    #   /bestseller/   -> bestseller page
    path("", include(("store.urls", "store"), namespace="store")),
]

# ============================================================
# MEDIA FILES SERVING (DEVELOPMENT ONLY)
# ============================================================
# Serve media files (user uploads) during development
# This allows accessing uploaded images at /media/products/image.jpg
#
# IMPORTANT: This only works when DEBUG=True (development mode)
# In production, configure your web server (Nginx, Apache) to serve media files
#
# static() function creates URL pattern for media files:
#   - MEDIA_URL: URL prefix (/media/)
#   - document_root: Directory where files are stored (MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Note: Static files (CSS, JS) are automatically served by Django during development
# No need to add anything here for static files
