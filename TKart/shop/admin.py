from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Orders, OrderUpdate #table name

admin.site.register(Product)
#we register our product

admin.site.register(Contact)

admin.site.register(Orders)

admin.site.register(OrderUpdate)