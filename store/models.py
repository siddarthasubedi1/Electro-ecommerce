"""
Store Models
============
This file defines all database models for the e-commerce store.
Models represent database tables and their relationships.
"""

from django.db import models


# ============================================================
# CATEGORY MODEL
# ============================================================
class Category(models.Model):
    """
    Category Model - Represents product categories (e.g., Electronics, Clothing)

    Fields:
        - name: The category name (max 50 characters)

    Usage:
        Used to organize products into different categories.
        One category can have multiple products (many-to-many relationship).
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        """String representation shown in admin panel and queries"""
        return self.name

    class Meta:
        # How it appears in Django admin (plural and singular)
        verbose_name_plural = "Categories"
        verbose_name = "Category"


# ============================================================
# TAG MODEL
# ============================================================
class Tag(models.Model):
    """
    Tag Model - Represents product tags for additional classification

    Fields:
        - name: The tag name (e.g., "Sale", "New", "Popular")

    Usage:
        Tags provide flexible product labeling beyond categories.
        Products can have multiple tags.
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        """String representation shown in admin panel and queries"""
        return self.name


# ============================================================
# PRODUCT MODEL
# ============================================================
class Product(models.Model):
    """
    Product Model - Main model for storing product information

    Fields:
        - name: Product name (max 50 characters)
        - old_price: Original price before discount (15 digits, 2 decimals)
        - price: Current selling price (15 digits, 2 decimals)
        - image: Product image file (stored in media/products/)
        - description: Detailed product description (unlimited text)
        - all_products: Boolean flag to show in "All Products" section
        - featured: Boolean flag to show in "Featured Products" section
        - new_arrivals: Boolean flag to show in "New Arrivals" section
        - top_selling: Boolean flag to show in "Top Selling" section
        - category: Many-to-Many relationship with Category model
        - tag: Many-to-Many relationship with Tag model
        - created_at: Timestamp when product was created (auto-set)
        - updated_at: Timestamp when product was last updated (auto-updated)

    Usage:
        Central model for all product data in the e-commerce store.
        Products can belong to multiple categories and have multiple tags.
    """

    name = models.CharField(max_length=50)
    old_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to="products/")  # Uploads to MEDIA_ROOT/products/
    description = models.TextField()  # No character limit

    # Boolean flags for product sections on the website
    all_products = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    new_arrivals = models.BooleanField(default=False)
    top_selling = models.BooleanField(default=False)

    # Relationships - Many-to-Many means one product can have multiple categories/tags
    # and one category/tag can have multiple products
    category = models.ManyToManyField(Category, related_name="products")
    tag = models.ManyToManyField(Tag, related_name="product_tags")

    # Auto-managed timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)  # Set once when created
    updated_at = models.DateTimeField(auto_now=True)  # Updated every time saved

    def __str__(self):
        """String representation shown in admin panel and queries"""
        return self.name


# ============================================================
# CART MODEL
# ============================================================
class Cart(models.Model):
    """
    Cart Model - Represents a user's shopping cart

    Fields:
        - user: One-to-One relationship with CustomUser
                (each user has exactly one cart)

    Relationship:
        - OneToOneField means each user can have only ONE cart
        - on_delete=CASCADE means if user is deleted, their cart is also deleted

    Usage:
        Stores which user owns the cart.
        Actual products are stored in CartProduct model (intermediate table).
    """

    user = models.OneToOneField(
        "accounts.CustomUser",  # Reference to CustomUser model in accounts app
        on_delete=models.CASCADE,  # Delete cart when user is deleted
    )

    def __str__(self):
        """String representation shown in admin panel and queries"""
        return f"{self.user.email}'s cart"


# ============================================================
# CARTPRODUCT MODEL (INTERMEDIATE TABLE)
# ============================================================
class CartProduct(models.Model):
    """
    CartProduct Model - Links products to carts with quantity

    This is an intermediate/junction table that connects Cart and Product
    with additional information (quantity).

    Fields:
        - product: Foreign key to Product (which product is in cart)
        - cart: Foreign key to Cart (which cart contains the product)
        - quantity: How many units of this product (positive integer)
        - added_at: When the product was added to cart (auto-set)

    Relationships:
        - ForeignKey to Product: Many cart items can reference one product
        - ForeignKey to Cart: One cart can have many cart items
        - on_delete=CASCADE: If product or cart is deleted, remove this entry

    Usage:
        This allows:
        - One cart to contain multiple different products
        - Each product in cart to have its own quantity
        - Track when each product was added to cart

    Example:
        Cart 1 -> CartProduct(product=iPhone, quantity=2)
        Cart 1 -> CartProduct(product=Laptop, quantity=1)
    """

    product = models.ForeignKey(
        Product,
        related_name="carts",  # Access from Product: product.carts.all()
        on_delete=models.CASCADE,  # Delete cart item if product is deleted
    )
    cart = models.ForeignKey(
        Cart,
        related_name="products",  # Access from Cart: cart.products.all()
        on_delete=models.CASCADE,  # Delete cart item if cart is deleted
    )
    quantity = models.PositiveIntegerField(default=1)  # Must be 1 or greater
    added_at = models.DateTimeField(auto_now_add=True)  # Set once when added

    # to get sub total price
    @property
    def get_total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        """String representation shown in admin panel and queries"""
        return f"{self.product.name} -> {self.cart.user}"
