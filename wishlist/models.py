from django.db import models
from django.contrib.auth.models import User


class Wishlist(models.Model):
    name = models.CharField(max_length=50, default='')
    user = models.ForeignKey(User, null=False)
    product_list = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.name
