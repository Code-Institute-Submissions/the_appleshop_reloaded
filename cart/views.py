from django.shortcuts import render, redirect, reverse
from .models import Cart
from django.contrib import messages


def view_cart(request):
    """A View that renders the cart contents page"""
    return render(request, "cart.html")


def add_to_cart(request, id):
    """Add a quantity of the specified product to the cart"""
    if not request.POST.get('quantity'):
        messages.success(request, "Please enter a value greater than 0")
        return redirect(reverse('products'))
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if id in cart:
        cart[id] = int(cart[id]) + quantity
    else:
        cart[id] = quantity
    request.session['cart'] = cart
    if request.user.is_authenticated:
        try:
            user_cart = Cart.objects.get(user=request.user.id)
        except:
            name = str(request.user)+"'s cart"
            user_cart = Cart(user=request.user, name=name, product_list="")
        user_cart.product_list = str(cart)
        user_cart.save()
    return redirect(reverse('products'))


def adjust_cart(request, id):
    """
    Adjust the quantity of the specified product to the specified
    amount
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[id] = quantity
    else:
        cart.pop(id)
    request.session['cart'] = cart
    if request.user.is_authenticated:
        try:
            user_cart = Cart.objects.get(user=request.user.id)
        except:
            name = str(request.user)+"'s cart"
            user_cart = Cart(user=request.user, name=name, product_list="")
        user_cart.product_list = str(cart)
        user_cart.save()
    return redirect(reverse('view_cart'))
