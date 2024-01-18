from itertools import product
from django.contrib.auth.models import User
from django.db import models

from product.models import Product

class Order(models.Model): # Modellen for ordre 
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = ( # Gir valg til "Status" feltet i ordre
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta: # Får ordrene til å sortere seg etter dato lagd
        ordering = ('-created_at',)

    def get_total_price(self): # Funksjon for å se total prisen i et ordre
        if self.paid_amount:
            return self.paid_amount
        
        return 0

class OrderItem(models.Model): # Modell for å vise hvem produkt kjøpt i et ordre
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.price
