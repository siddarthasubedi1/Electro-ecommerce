"""
Store Admin Configuration
==========================
This file registers models with Django's admin interface.

Django Admin:
- Automatic admin interface for managing database records
- Access at http://localhost:8000/admin/
- Only superusers can access (create with: python manage.py createsuperuser)

Purpose:
- Register models so they appear in admin panel
- Allows staff to add/edit/delete products, categories, etc.
- Can be customized with ModelAdmin classes for advanced features
"""

from django.contrib import admin
from .models import Category, Product, Tag, Cart, CartProduct

# ============================================================
# REGISTER MODELS FOR ADMIN INTERFACE
# ============================================================

# Register Category model - manage product categories
admin.site.register(Category)

# Register Product model - manage all products
# This is the main model where you add/edit products
admin.site.register(Product)

# Register Tag model - manage product tags
admin.site.register(Tag)

# Register Cart model - view/manage user shopping carts
admin.site.register(Cart)

# Register CartProduct model - view/manage items in carts
# Shows the relationship between carts and products with quantities
admin.site.register(CartProduct)

# Note: For more advanced admin features, you can create ModelAdmin classes:
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'created_at']
#     list_filter = ['category', 'featured']
#     search_fields = ['name', 'description']
# admin.site.register(Product, ProductAdmin)
