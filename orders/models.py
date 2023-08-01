from django.db import models

import random
import string
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from store.models import Product


def rand_slug():
    return ''.join(random.choice(string.ascii_uppercase  + string.digits) for _ in range(10))

class Order(models.Model):
    STATUS = (
        ('Pending, awaiting payment', 'Pending, awaiting payment'),
        ('Shipping in Progress', 'Shipping in Progress'),
        ('Delivered', 'Delivered'),
        ('Stopped by custom', 'Stopped by custom'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='order_user' , null=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    paid = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    sub_total = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    order_key = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=150, choices=STATUS, default='Pending, awaiting payment')

    class Meta:
        ordering = ('-created',)

    def get_final_balance(self):
        return self.total - self.paid
    
    def __str__(self):
        return str(self.created)


def order_key_post_save(sender, instance, created,*args, **kwargs):
    if created:
        ref_final = f'{rand_slug()}{instance.id}'
        instance.order_key = f'BR-{ref_final}-INC'
        instance.save()

post_save.connect(order_key_post_save, sender=Order)



class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
