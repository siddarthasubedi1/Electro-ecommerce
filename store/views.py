"""
Store Views
===========
This file contains all view functions for the e-commerce store.
Views handle HTTP requests and return HTTP responses (usually rendered HTML templates).

Key Concepts:
- request: Object containing HTTP request data (GET parameters, POST data, user info, etc.)
- context: Dictionary of data passed to templates for rendering
- redirect: Send user to a different URL
- render: Combine template with context data to create HTML response
"""

from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FilterProductForm
from django.urls import reverse, reverse_lazy
from .models import Product, Category, Cart, CartProduct
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ============================================================
# HELPER FUNCTION
# ============================================================
def _get_cart_product_ids(request):
    """
    Helper function to get list of product IDs currently in user's cart.

    Purpose:
        - Used to highlight "Added to Cart" products in product listings
        - Shows which products are already in the cart

    Parameters:
        - request: HTTP request object containing user information

    Returns:
        - List of product IDs (integers) that are in the user's cart
        - Empty list [] if user is not logged in or has no cart

    Logic Flow:
        1. Check if user is authenticated (logged in)
        2. If not logged in, return empty list
        3. Get user's cart from database
        4. If no cart exists, return empty list
        5. Get all products in cart and extract their IDs
        6. Return list of product IDs
    """
    if not request.user.is_authenticated:
        return []

    # Try to get the cart for this user (returns None if doesn't exist)
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return []

    # Get all CartProduct entries for this cart and extract product IDs
    # flat=True returns a simple list instead of tuples
    return list(
        CartProduct.objects.filter(cart=cart).values_list("product_id", flat=True)
    )


# ============================================================
# HOME PAGE VIEW
# ============================================================
def home(request):
    """
    Home page view - Displays different product sections on homepage.

    URL: / (root URL)
    Template: store/home.html

    Purpose:
        - Show various product collections (featured, new arrivals, top selling)
        - Each section can display different products

    Query Explanation:
        - Product.objects.all(): Get all products from database
        - .filter(featured=True): Only get products where featured=True
        - .order_by("-created_at"): Sort by created_at in descending order
                                    (- means descending, newest first)

    Context Variables (sent to template):
        - products: All products
        - all_products: Products marked as "all_products"
        - featured_products: Products marked as "featured"
        - new_arrivals_products: Products marked as "new_arrivals"
        - top_selling_products: Products marked as "top_selling"
        - cart_product_ids: List of product IDs in user's cart
        - featured/new_arrivals/top_selling: Backward-compatible aliases
    """
    products = Product.objects.all().order_by("-created_at")
    all_products = Product.objects.filter(all_products=True).order_by("-created_at")
    featured_products = Product.objects.filter(featured=True).order_by("-created_at")
    new_arrivals_products = Product.objects.filter(new_arrivals=True).order_by(
        "-created_at"
    )
    top_selling_products = Product.objects.filter(top_selling=True).order_by(
        "-created_at"
    )

    context = {
        "products": products,
        "all_products": all_products,
        "featured_products": featured_products,
        "new_arrivals_products": new_arrivals_products,
        "top_selling_products": top_selling_products,
        "cart_product_ids": _get_cart_product_ids(request),
        # Backwards-compatible names (in case templates still reference them)
        "featured": featured_products,
        "new_arrivals": new_arrivals_products,
        "top_selling": top_selling_products,
    }
    return render(request, "store/home.html", context)


# ============================================================
# PRODUCT LISTING & FILTERING VIEW
# ============================================================
def product(request):
    """
    Product listing page with filtering and pagination.

    URL: /shop/
    Template: store/shop.html

    Purpose:
        - Display all products with filtering options (name, category, price range)
        - Support search functionality
        - Sort products by different criteria
        - Paginate results (8 products per page)

    GET Parameters:
        - search: Search query from header search bar
        - name: Product name filter from filter form
        - categories: List of category IDs to filter by
        - min_price: Minimum price filter
        - max_price: Maximum price filter
        - sorting_key: How to sort products (price_asc, price_dec, latest, oldest)
        - page: Page number for pagination

    Logic Flow:
        1. Get all products from database
        2. Copy GET parameters and handle search vs name parameter
        3. Validate form data
        4. Apply filters (name, categories, price range)
        5. Apply sorting
        6. Check if filters returned no results
        7. Paginate results (8 per page)
        8. Send data to template
    """
    products = Product.objects.all().order_by("-created_at")

    # Handle both header search (?search=...) and filter form (?name=...)
    # Copy GET data so we can modify it without affecting the original
    data = request.GET.copy()
    # Header search uses `search=...` while FilterProductForm expects `name=...`
    if data.get("search") and not data.get("name"):
        data["name"] = data.get("search")

    filter_form = FilterProductForm(data)
    no_results = False  # Flag to show "No products found" message

    # Check if form data is valid (correct data types, within limits, etc.)
    if filter_form.is_valid():
        # Extract cleaned (validated) data from form
        name = filter_form.cleaned_data.get("name")
        categories = filter_form.cleaned_data.get("categories")
        min_price = filter_form.cleaned_data.get("min_price")
        max_price = filter_form.cleaned_data.get("max_price")
        sorting_key = filter_form.cleaned_data.get("sorting_key")

        # Apply name filter (case-insensitive partial match)
        # icontains: case-insensitive contains ("iPhone" matches "iphone 12")
        if name:
            products = products.filter(name__icontains=name)

        # Apply category filter
        # __in: SQL IN operator (category is in the list of selected categories)
        # .distinct(): Remove duplicate products (since ManyToMany can create duplicates)
        if categories:
            products = products.filter(category__in=categories).distinct()

        # Apply minimum price filter
        # __gte: Greater Than or Equal to
        if min_price is not None:
            products = products.filter(price__gte=min_price)

        # Apply maximum price filter
        # __lte: Less Than or Equal to
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        # Apply sorting based on user selection
        if sorting_key:
            if sorting_key == "price_asc":
                products = products.order_by("price")  # Low to high
            elif sorting_key == "price_dec":
                products = products.order_by(
                    "-price"
                )  # High to low (- means descending)
            elif sorting_key == "latest":
                products = products.order_by("-created_at")  # Newest first
            elif sorting_key == "oldest":
                products = products.order_by("created_at")  # Oldest first
            # "popularity" left as default for now (no separate field)

        # Check if filters were applied but returned no results
        if (
            name or categories or min_price or max_price or sorting_key
        ) and not products.exists():
            no_results = True
            # Keep empty queryset so the template can show "No products found"

    # Pagination: Split products into pages of 8 items each
    # Paginator creates page objects from the products queryset
    paginated_products = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get("page")  # Get current page number from URL
    page_obj = paginated_products.get_page(page_number)  # Get the page object
    totalpage = page_obj.paginator.num_pages  # Total number of pages

    context = {
        "products": page_obj,  # Current page of products
        "filter_form": filter_form,  # Form with current filter values
        "no_results": no_results,  # Flag for "no results" message
        "lastpage": totalpage,  # Total number of pages
        "totalpagelist": [
            n + 1 for n in range(totalpage)
        ],  # [1, 2, 3, ...] for pagination
        "cart_product_ids": _get_cart_product_ids(request),  # Products in cart
    }
    return render(request, "store/shop.html", context)


# ============================================================
# BESTSELLER VIEW
# ============================================================
def bestseller(request):
    """
    Bestseller page - Shows only top selling products.

    URL: /bestseller/
    Template: store/shop.html (same as product listing)

    Purpose:
        - Display products marked as top_selling=True
        - Sorted by newest first

    Note:
        - Uses same template as product() view but with filtered products
        - No pagination or filtering applied (shows all top sellers)
    """
    products = Product.objects.filter(top_selling=True).order_by("-created_at")

    context = {
        "products": products,
        "cart_product_ids": _get_cart_product_ids(request),
    }
    return render(request, "store/shop.html", context)


# ============================================================
# PRODUCT DETAIL VIEW
# ============================================================
def product_detail(request, pk: int):
    """
    Product detail page - Shows detailed information for a single product.

    URL: /product/<id>/detail/
    Template: store/product_detail.html

    Parameters:
        - pk (int): Primary key (ID) of the product to display
                    Comes from URL pattern <int:pk>

    Purpose:
        - Display full product information (description, images, price, etc.)
        - Show add to cart button
        - Show if product is already in cart

    Error Handling:
        - get_object_or_404: Returns 404 error page if product doesn't exist
          Instead of crashing, shows user a "Page Not Found" error
    """
    product = get_object_or_404(Product, pk=pk)  # Get product or show 404 error
    context = {
        "product": product,
        "cart_product_ids": _get_cart_product_ids(request),  # To show "in cart" status
    }
    return render(request, "store/product_detail.html", context)


# ============================================================
# ADD TO CART VIEW
# ============================================================
@login_required(login_url=reverse_lazy("accounts:loginpage"))
def add_to_cart(request, pk):
    """
    Add a product to user's shopping cart.

    URL: /cart/<product_id>/add
    Method: GET or POST
    Decorator: @login_required - User must be logged in to access this view

    Parameters:
        - pk (int): Primary key (ID) of the product to add to cart
        - quantity (int, optional): Quantity to add (from POST data, defaults to 1)

    Purpose:
        - Add product to cart with specified quantity
        - If product already in cart, add to existing quantity
        - Show success/info messages to user
        - Redirect back to previous page

    Logic Flow:
        1. Check if user is authenticated (decorator handles this)
        2. Get the product or show 404 error
        3. Get quantity from POST data (default 1)
        4. Get or create cart for this user
        5. Get or create CartProduct entry
        6. If product already in cart, add to existing quantity
        7. If new product, add with specified quantity
        8. Show appropriate message
        9. Redirect to previous page (or product detail page)

    Database Operations:
        - get_or_create(): Try to get record, if doesn't exist, create it
          Returns: (object, created) where created is True if new, False if existed

    Messages:
        - messages.success(): Green success message shown to user
        - messages.info(): Blue info message shown to user
    """
    # Double-check authentication (though decorator should handle this)
    if not request.user.is_authenticated:
        messages.info(request, "Please login to add products to your cart")
        return redirect("accounts:loginpage")

    # Get the product or return 404 error if not found
    product = get_object_or_404(Product, pk=pk)
    logged_in_user = request.user

    # Get quantity from POST data, default to 1
    quantity = 1
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity < 1:
                quantity = 1
            elif quantity > 99:
                quantity = 99
        except (ValueError, TypeError):
            quantity = 1

    # Get user's cart, or create one if they don't have a cart yet
    # get_or_create returns (cart_object, created_boolean)
    # We only need cart_object, so we use _ for the boolean
    cart, _ = Cart.objects.get_or_create(user=logged_in_user)

    # Try to get existing CartProduct entry for this cart and product
    # If doesn't exist, create it with specified quantity (defaults parameter)
    cart_item, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},  # Only used if creating new entry
    )

    if not created:
        # Product was already in cart, so add to existing quantity
        cart_item.quantity += quantity
        cart_item.save(
            update_fields=["quantity"]
        )  # Only save quantity field (more efficient)
        messages.info(
            request, f"Added {quantity} more to cart (Total: {cart_item.quantity})"
        )
    else:
        # New product was added to cart
        messages.success(request, f"Added {quantity} {product.name} to cart")

    # Redirect to previous page (where user came from)
    # HTTP_REFERER contains the previous page URL
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)  # Go back to previous page

    # Fallback: if no referer, redirect to product detail page
    return redirect("store:product_detail", pk=pk)


# ============================================================
# CART VIEW
# ============================================================
@login_required
def cart(request):
    """
    Shopping cart page - Display logged-in user's cart contents.

    URL: /cart/
    Template: store/cart.html

    Purpose:
        - Display all products in user's cart
        - Show quantities and prices
        - Allow user to update quantities or remove items
        - Show total price

    Logic:
        - If user is logged in, show their cart
        - If not logged in, redirect to login page
    """

    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    try:
        cart_product = CartProduct.objects.filter(cart=user_cart)

        # Calculate subtotal (sum of all item prices)
        subtotal = 0
        for cart_item in cart_product:
            subtotal += cart_item.get_total_price

        # Calculate tax (13%)
        tax = subtotal * Decimal("0.13")

        # Calculate total (subtotal + tax)
        total = subtotal + tax

    except Exception as e:
        messages.error(request, "Something went wrong loading your cart")
        return redirect("store:homepage")

    context = {
        "products": cart_product,
        "subtotal": subtotal,  # Cart subtotal
        "tax": tax,  # 13% tax
        "total": total,  # Final total with tax
        "cart_items": cart_product.exists(),  # Boolean to check if cart has items
    }

    return render(
        request,
        "store/cart.html",
        context,
    )


# Remove cart product means delete
@login_required
def remove_from_cart(request, pk):
    """
    Remove a product from user's shopping cart.

    URL: /cart/<cart_item_id>/remove
    Method: POST (for security)
    Decorator: @login_required - User must be logged in

    Parameters:
        - pk (int): Primary key (ID) of the CartProduct to remove

    Security:
        - Only accepts POST requests
        - Verifies cart item belongs to current user before deleting
        - Prevents users from deleting other users' cart items
    """
    if request.method == "POST":
        try:
            # Get the cart item and verify it belongs to the current user's cart
            cart_item = CartProduct.objects.get(pk=pk, cart__user=request.user)
            cart_item.delete()
            messages.success(request, "Cart item deleted successfully.")
        except CartProduct.DoesNotExist:
            messages.error(request, "Cart item doesn't exist or doesn't belong to you.")
        except Exception as e:
            print(e)
            messages.error(request, "Removing item from cart failed.")

    return redirect("store:cart")


# Update cart product quantity
@login_required
def update_cart_quantity(request, pk):
    """
    Update quantity of a product in user's shopping cart.

    URL: /cart/<cart_item_id>/update
    Method: POST
    Decorator: @login_required - User must be logged in

    Parameters:
        - pk (int): Primary key (ID) of the CartProduct to update
        - action (str): 'increase' or 'decrease' from POST data

    Security:
        - Only accepts POST requests
        - Verifies cart item belongs to current user before updating
        - Prevents users from updating other users' cart items

    Logic:
        - If action is 'increase', add 1 to quantity
        - If action is 'decrease', subtract 1 from quantity
        - If quantity becomes 0 or less, delete the item
        - Maximum quantity is 99
    """
    if request.method == "POST":
        try:
            # Get the cart item and verify it belongs to the current user's cart
            cart_item = CartProduct.objects.get(pk=pk, cart__user=request.user)
            action = request.POST.get("action")

            if action == "increase":
                if cart_item.quantity < 99:
                    cart_item.quantity += 1
                    cart_item.save(update_fields=["quantity"])
                    messages.success(request, "Quantity increased")
                else:
                    messages.warning(request, "Maximum quantity is 99")
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save(update_fields=["quantity"])
                    messages.success(request, "Quantity decreased")
                else:
                    # If quantity is 1 and user decreases, remove item
                    cart_item.delete()
                    messages.success(request, "Item removed from cart")

        except CartProduct.DoesNotExist:
            messages.error(request, "Cart item doesn't exist or doesn't belong to you.")
        except Exception as e:
            print(e)
            messages.error(request, "Updating cart quantity failed.")

    return redirect("store:cart")
