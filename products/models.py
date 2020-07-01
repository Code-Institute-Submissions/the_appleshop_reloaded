from django.db import models


class Product(models.Model):
    USE_CHOICES = (('eat', 'eat'), ('cook', 'cook'))
    FRUIT_CHOICES = (('apple', 'apple'), ('pear', 'pear'))
    name = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    origin = models.CharField(max_length=20, default='', blank=False)
    first_developed = models.CharField(max_length=4, default='', blank=False)
    description = models.TextField()
    use = models.CharField(max_length=10, choices=USE_CHOICES, default='')
    view_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=254, default='')
    fruit = models.CharField(max_length=10, default='', choices=FRUIT_CHOICES)
    ordered_pcs = models.IntegerField(default=0)

    def __str__(self):
        return self.name
