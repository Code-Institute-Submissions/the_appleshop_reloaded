from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    title = models.CharField(max_length=50, default='', blank=False)
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=100, default='', blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    author = models.ForeignKey(User)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=False)
    comment = models.TextField(blank=False)
    view_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
