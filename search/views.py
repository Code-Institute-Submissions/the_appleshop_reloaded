from django.shortcuts import render
from products.models import Product
from reviews.models import Review


def product_search(request):
    searchterm = request.GET.get('q', "")
    products = Product.objects.filter(name__icontains=searchterm)
    return render(request, 'products.html', {'products': products,
                                             'searchterm': 'searchterm'})


def review_search(request):
    searchterm = request.GET.get('q', "")
    reviews = Review.objects.filter(name__icontains=searchterm)
    return render(request, 'reviews.html', {'reviews': reviews,
                                            'searchterm': 'searchterm'})
