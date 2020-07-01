from django.shortcuts import get_object_or_404
from products.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from django.contrib import messages


def wishlist_contents(request):
    """
    Ensures that the wishlist contents are available when rendering
    every page
    """
    if request.user.is_authenticated:
        sync_wishlists(request)
    wishlist = request.session.get('wishlist', [])
    wishlist_items = []
    for id in wishlist:
        product = get_object_or_404(Product, pk=id)
        wishlist_items.append({'product': product})
    return {'wishlist': wishlist, 'wishlist_items': wishlist_items,
            'wishlist_count': len(wishlist)}


def make_wishlist_string(wishlist):
        return ','.join(str(product_id) for product_id in wishlist)


def make_wishlist_list(productlist):
    if productlist != "":
        tmplist = productlist.split(',')
        tmp_wishlist = [int(product) for product in tmplist]
        return tmp_wishlist
    else:
        return []


def merge_wishlists(tmp_wishlist_from_db, wishlist):
    merged_wishlist = wishlist
    for product in tmp_wishlist_from_db:
        if product not in merged_wishlist:
            merged_wishlist.append(product)
    return merged_wishlist


@login_required
def sync_wishlists(request):
    wishlist = request.session.get('wishlist', [])
    user_wishlist = None
    try:
        user_wishlist = Wishlist.objects.get(user=request.user.id)

    except:
        messages.success(request, "Saving wishlist to database")
        name = str(request.user)+"'s wishlist"
        user_wishlist = Wishlist(user=request.user, name=name, product_list="")
        user_wishlist.save()

    if user_wishlist.product_list != "":
        if wishlist == []:
            request.session['wishlist'] = make_wishlist_list(user_wishlist
                                                             .product_list)

        else:
            tmp_wishlist_db = make_wishlist_list(user_wishlist.product_list)
            merged_wishlist = merge_wishlists(tmp_wishlist_db, wishlist)
            user_wishlist.product_list = make_wishlist_string(merged_wishlist)
            user_wishlist.save()
            request.session['wishlist'] = merged_wishlist

    elif user_wishlist.product_list == "":
        if wishlist != []:
            user_wishlist.product_list = make_wishlist_string(wishlist)
            user_wishlist.save()
    return
