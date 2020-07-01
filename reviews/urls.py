from django.conf.urls import url
from .views import get_reviews, review_detail, edit_review, create_review, delete_review

urlpatterns = [
    url(r'^$', get_reviews, name='get_reviews'),
    url(r'^(?P<pk>\d+)/$', review_detail, name='review_detail'),
    url(r'^new/(?P<pk>\d+)$', create_review, name='new_review'),
    url(r'^(?P<pk>\d+)/edit/$', edit_review, name='edit_review'),
    url(r'^(?P<pk>\d+)/delete/$', delete_review, name='delete_review'),
]
