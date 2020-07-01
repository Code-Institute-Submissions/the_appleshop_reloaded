from django.conf.urls import url
from .views import product_search, review_search

urlpatterns = [
    url(r'^product_search/$', product_search, name='product_search'),
    url(r'^review_search/$', review_search, name='review_search'),
]
