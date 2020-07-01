from django.shortcuts import render, redirect
from products.models import Product


def index(request):
    """
    A view that displays an index page, in this case the overview of
    bestsellers
    """
    products = Product.objects.filter(ordered_pcs__gt=99).order_by('-ordered_pcs')[:3]
    return render(request, 'bestsellers.html', {'products': products})
