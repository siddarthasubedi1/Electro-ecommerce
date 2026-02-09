from django import forms
from .models import Product, Category


SORTING_CHOICES = [
    ("", "Default"),
    ("price_asc", "Price Low to high"),
    ("price_dec", "Price Hign to low"),
    ("latest", "Latest"),
    ("oldest", "Oldest"),
]


class FilterProductForm(forms.Form):
    name = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control border-0 py-3 ps-4",
                "placeholder": "Search products...",
                "aria-label": "Search products",
            },
        ),
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', })
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', })
    )
    
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        required =False,
        widget= forms.CheckboxSelectMultiple(attrs={'class':''})
    )

    sorting_key = forms.ChoiceField(
        choices=SORTING_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select form-select-sm border-0 bg-white w-auto",
            }
        ),
    )
