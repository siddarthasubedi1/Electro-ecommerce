"""
Store Forms
===========
This file defines forms for user input in the store app.

Forms in Django:
- Validate user input (data validation, security)
- Generate HTML form fields with proper attributes
- Clean and process submitted data
- Display errors to users
"""

from django import forms
from .models import Product, Category


# ============================================================
# SORTING CHOICES CONSTANT
# ============================================================
# List of tuples: (value_stored_in_database, label_shown_to_user)
# Used in the sorting dropdown on product listing page
SORTING_CHOICES = [
    ("", "Default"),  # Empty value means no specific sorting
    ("price_asc", "Price Low to high"),  # Sort by price ascending
    ("price_dec", "Price High to low"),  # Sort by price descending
    ("latest", "Latest"),  # Sort by newest products first
    ("oldest", "Oldest"),  # Sort by oldest products first
]


# ============================================================
# PRODUCT FILTER FORM
# ============================================================
class FilterProductForm(forms.Form):
    """
    Form for filtering and searching products on the shop page.

    This is a regular Form (not ModelForm) because it's not directly
    tied to saving/updating a single model instance.

    Fields:
        - name: Text search for product names
        - min_price: Minimum price filter (decimal)
        - max_price: Maximum price filter (decimal)
        - categories: Multiple category selection (checkboxes)
        - sorting_key: Sorting dropdown (price, date, etc.)

    All fields are optional (required=False) so users can filter
    by any combination of criteria or none at all.
    """

    # ========== NAME SEARCH FIELD ==========
    # CharField: Text input for searching product names
    # required=False: User doesn't have to fill this field
    # widget: Customizes how the HTML input field appears
    name = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(
            attrs={  # HTML attributes added to the <input> tag
                "class": "form-control border-0 py-3 ps-4",  # Bootstrap CSS classes
                "placeholder": "Search products...",  # Placeholder text
                "aria-label": "Search products",  # Accessibility label
            },
        ),
    )

    # ========== MINIMUM PRICE FILTER ==========
    # DecimalField: For decimal numbers (prices)
    # max_digits=10: Total digits (both before and after decimal)
    # decimal_places=2: Exactly 2 digits after decimal (e.g., 99.99)
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",  # Bootstrap styling
            }
        ),
    )

    # ========== MAXIMUM PRICE FILTER ==========
    # Same as min_price but for upper limit
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",  # Bootstrap styling
            }
        ),
    )

    # ========== CATEGORY FILTER ==========
    # ModelMultipleChoiceField: Select multiple categories from database
    # queryset: All categories from database to choose from
    # widget=CheckboxSelectMultiple: Show as checkboxes instead of dropdown
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # Get all categories from database
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": ""}),
    )

    # ========== SORTING DROPDOWN ==========
    # ChoiceField: Select one option from predefined choices
    # choices: Uses SORTING_CHOICES constant defined above
    # widget=Select: Renders as <select> dropdown
    sorting_key = forms.ChoiceField(
        choices=SORTING_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select form-select-sm border-0 bg-white w-auto",
            }
        ),
    )
