from django.conf.urls import url, include
from .views import view_wishlist, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    url(r'^$', view_wishlist, name='view_wishlist'),
    url(r'^add/(?P<id>\d+)', add_to_wishlist, name='add_to_wishlist'),
    url(r'^remove/(?P<id>\d+)', remove_from_wishlist,
        name='remove_from_wishlist'),
]
