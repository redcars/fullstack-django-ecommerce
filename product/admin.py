from django.contrib import admin

from .models import Category, Product


# Sender modeller fra databasen til administrasjons siden for å kunne manipuleres
admin.site.register(Category)
admin.site.register(Product)



