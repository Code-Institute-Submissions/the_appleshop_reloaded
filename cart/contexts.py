from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart
import yaml


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering
    every page
    """
    cart = request.session.get('cart', {})
    if request.user.is_authenticated:
        sync_carts(request)
    shippingfee = 8
    cart_items = []
    total = 0
    product_count = 0
    for id, quantity in cart.items():
        product = get_object_or_404(Product, pk=id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})
    if total < 50:
        total += shippingfee
    else:
        shippingfee = "FREE"

    return {'cart_items': cart_items, 'total': total, 'product_count':
            product_count, 'shippingfee': shippingfee}


"""
method not in use anymore as I found dictionary conversion
into string and converting back to dictionary with yaml better
to store whole cart content into one field in db. But splitting
the cart dictionary into two strings (one for keys and one for values)
to make it fit for a CharField worked too, same as for re-conversion
from string to dictionary.

def make_cart_strings(cart):
        idstring=""
        quantitystring=""
        for k,v in cart.items():
            idstring+=str(k)+","
            quantitystring+=str(v)+","
        return (idstring, quantitystring)


def make_cart_dict(productstring, quantitystring):
    idlist = productstring.split(',')
    idlist.pop(len(idlist)-1)
    quantitylist = quantitystring.split(',')
    quantitylist.pop(len(quantitylist)-1)
    quantitylist_iter = iter(quantitylist)
    newcart = {}
    for id in idlist:
        newcart[id]=next(quantitylist_iter)
    return newcart
"""


def merge_carts(tmp_cart_from_db, cart):
    merged_cart = cart
    quantity_change = False

    for id, quantity in tmp_cart_from_db.items():
        if id not in merged_cart:
            merged_cart[id] = quantity
        elif id in merged_cart:
            if tmp_cart_from_db[id] > merged_cart[id]:
                merged_cart[id] = quantity
                quantity_change = True
    return merged_cart, quantity_change


@login_required
def sync_carts(request):
    cart = request.session.get('cart', {})
    user_cart = None

    try:
        user_cart = Cart.objects.get(user=request.user.id)
    except:
        messages.success(request, "Saving cart to database")
        name = str(request.user)+"'s cart"
        user_cart = Cart(user=request.user, name=name, product_list="")
        user_cart.save()

    if user_cart.product_list != "":
        if cart == {}:
            request.session['cart'] = yaml.load(user_cart.product_list,
                                                Loader=yaml.FullLoader)
        else:
            tmp_cart_db = yaml.load(user_cart.product_list,
                                    Loader=yaml.FullLoader)
            tmp_merged_cart = merge_carts(tmp_cart_db, cart)
            merged_cart = tmp_merged_cart[0]
            quantity_change = tmp_merged_cart[1]
            user_cart.product_list = str(merged_cart)
            user_cart.save()
            request.session['cart'] = merged_cart
            if quantity_change:
                messages.success(request, "Order quantity has been updated for \
                                 someproducts with higher value.")

    elif user_cart.product_list == "":
        if cart != {}:
            user_cart.product_list = str(cart)
            user_cart.save()
    return
