from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product
from checkout.models import OrderLineItem
from django.contrib import messages


def get_user_purchases(user):
    """
    Pulls user's purchased products from the past. Used to check if customer
    is eligible to review a product.
    """
    purchased_products = []
    orderline_items = OrderLineItem.objects.filter(user=user)
    if orderline_items:
        for lineitem in orderline_items:
            purchased_products.append(str(lineitem.product.name))
    return purchased_products


def all_products(request):
    """
    Retrieves all products to render the all products overview.
    """
    products = Product.objects.all()
    purchased_products = []
    if request.user.is_authenticated:
        purchased_products = get_user_purchases(request.user)
    return render(request, 'products.html',
                  {'products': products, 'purchased_products':
                   purchased_products})


def product_detail(request, id):
    """
    Retrieves product details and checks if the given product has been
    purchased by logged on user (so a review button can be offered). 
    """
    try:
        product = get_object_or_404(Product, pk=id)

    except:
        messages.error(request, "Sorry, this product does not exist")
        return redirect(reverse('products'))

    product.view_count += 1
    product.save()
    purchased_products = []
    if request.user.is_authenticated:
        purchased_products = get_user_purchases(request.user)
    return render(request, "productdetail.html",
                  {'product': product, 'purchased_products':
                   purchased_products})
