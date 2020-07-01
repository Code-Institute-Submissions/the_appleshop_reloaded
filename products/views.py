from django.shortcuts import render, get_object_or_404
from .models import Product
from checkout.models import OrderLineItem


def get_user_purchases(user):
    purchased_products = []
    orderline_items = OrderLineItem.objects.filter(user=user)
    if orderline_items:
        for lineitem in orderline_items:
            purchased_products.append(str(lineitem.product.name))
    return purchased_products


def all_products(request):
    products = Product.objects.all()
    purchased_products = []
    if request.user.is_authenticated:
        purchased_products = get_user_purchases(request.user)
    return render(request, 'products.html',
                  {'products': products, 'purchased_products':
                   purchased_products})


def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    product.view_count += 1
    product.save()
    purchased_products = []
    if request.user.is_authenticated:
        purchased_products = get_user_purchases(request.user)
    return render(request, "productdetail.html",
                  {'product': product, 'purchased_products':
                   purchased_products})
