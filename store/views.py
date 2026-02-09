from django.shortcuts import get_object_or_404, render
from .forms import FilterProductForm
from .models import Product,Category
from django.core.paginator import Paginator

def home(request):
    products = Product.objects.all().order_by('-created_at')
    all_products = Product.objects.filter(all_products=True).order_by('-created_at')
    featured_products = Product.objects.filter(featured=True).order_by('-created_at')
    new_arrivals_products = Product.objects.filter(new_arrivals=True).order_by('-created_at')
    top_selling_products = Product.objects.filter(top_selling=True).order_by('-created_at')

    context = {
        "products": products,
        "all_products": all_products,
        "featured_products": featured_products,
        "new_arrivals_products": new_arrivals_products,
        "top_selling_products": top_selling_products,

        # Backwards-compatible names (in case templates still reference them)
        "featured": featured_products,
        "new_arrivals": new_arrivals_products,
        "top_selling": top_selling_products,
    }
    return render (request, 'store/home.html',context)


def product(request):
    products = Product.objects.all().order_by('-created_at')

    data = request.GET.copy()
    # Header search uses `search=...` while FilterProductForm expects `name=...`
    if data.get('search') and not data.get('name'):
        data['name'] = data.get('search')

    filter_form = FilterProductForm(data)
    no_results = False

    if filter_form.is_valid():
        name = filter_form.cleaned_data.get('name')
        categories = filter_form.cleaned_data.get('categories')
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        sorting_key = filter_form.cleaned_data.get('sorting_key')

        if name:
            products = products.filter(name__icontains=name)

        if categories:
            products = products.filter(category__in=categories).distinct()

        if min_price is not None:
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            products = products.filter(price__lte=max_price)

        if sorting_key:
            if sorting_key == "price_asc":
                products = products.order_by("price")
            elif sorting_key == "price_dec":
                products = products.order_by("-price")
            elif sorting_key == "latest":
                products = products.order_by("-created_at")
            elif sorting_key == "oldest":
                products = products.order_by("created_at")
            # "popularity" left as default for now (no separate field)

        if (name or categories or min_price or max_price or sorting_key) and not products.exists():
            no_results = True
            # Keep empty queryset so the template can show "No products found"
    paginated_products = Paginator(products, 4)
    page_number = request.GET.get("page")
    page_obj = paginated_products.get_page(page_number)
    context = {
        "products": products,
        'filter_form': filter_form,
        'no_results': no_results,
    }
    return render(request, "store/shop.html", context)


def bestseller(request):
    products = Product.objects.filter(top_selling=True).order_by('-created_at')

    context = {
        "products": products,
        
    }
    return render(request, "store/shop.html", context)


def product_detail(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product,
    }
    return render(request, "store/product_detail.html", context)
