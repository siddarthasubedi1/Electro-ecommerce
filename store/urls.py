"""
Store URL Configuration
=======================
This file maps URLs to view functions for the store app.

URL Patterns:
- When a user visits a URL, Django matches it against these patterns
- If match found, Django calls the associated view function
- The view function returns an HTTP response (HTML page)

Key Concepts:
- path(route, view, name): Basic URL pattern
- <int:pk>: Captures an integer from URL and passes it as 'pk' parameter
- app_name: Namespace for URLs (use as 'store:homepage' in templates)
"""

from django.urls import path
from . import views

# Namespace for these URLs - allows us to use {% url 'store:homepage' %}
app_name = "store"

urlpatterns = [
    # ========== HOME PAGE ==========
    # URL: /  (root URL of store app)
    # View: home() in views.py
    # Name: 'homepage' - use in templates as {% url 'store:homepage' %}
    path("", views.home, name="homepage"),
    # ========== SHOP/PRODUCT LISTING PAGE ==========
    # URL: /shop/
    # View: product() - shows all products with filtering
    # Name: 'shoppage'
    path("shop/", views.product, name="shoppage"),
    # ========== PRODUCT DETAIL PAGE ==========
    # URL: /product/123/detail/  (where 123 is the product ID)
    # <int:pk>: Captures integer from URL, passes as 'pk' parameter to view
    # Example: /product/5/detail/ calls product_detail(request, pk=5)
    # View: product_detail(request, pk)
    # Name: 'product_detail'
    path("product/<int:pk>/detail/", views.product_detail, name="product_detail"),
    # ========== BESTSELLER PAGE ==========
    # URL: /bestseller/
    # View: bestseller() - shows only top selling products
    # Name: 'bestseller'
    path("bestseller/", views.bestseller, name="bestseller"),
    # ========== ADD TO CART ==========
    # URL: /cart/123/add  (where 123 is the product ID)
    # Example: /cart/5/add adds product with ID 5 to cart
    # View: add_to_cart(request, pk)
    # Name: 'cartpage' (note: might be better named 'add_to_cart')
    path("cart/<int:pk>/add", views.add_to_cart, name="cartpage"),
    # ========== VIEW CART ==========
    # URL: /cart/
    # View: cart(request) - displays logged-in user's cart
    # Name: 'cart'
    # Each user sees their own cart (no pk needed)
    path("cart/", views.cart, name="cart"),
    # ========== REMOVE FROM CART ==========
    # URL: /cart/123/remove  (where 123 is the CartProduct ID)
    # View: remove_from_cart(request, pk) - deletes cart item
    # Name: 'remove_from_cart'
    path("cart/<int:pk>/remove", views.remove_from_cart, name="remove_from_cart"),
    # ========== UPDATE CART QUANTITY ==========
    # URL: /cart/123/update  (where 123 is the CartProduct ID)
    # View: update_cart_quantity(request, pk) - updates item quantity
    # Name: 'update_cart_quantity'
    path(
        "cart/<int:pk>/update", views.update_cart_quantity, name="update_cart_quantity"
    ),
    # ========== CHECKOUT (COMMENTED OUT) ==========
    # Future feature: Payment and order processing
    # Uncomment when checkout functionality is implemented
    # path("checkout/", views.checkout, name="checkout"),
]
