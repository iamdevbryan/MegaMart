from django.contrib import admin
from .models import Product, Order, OrderItem, Shop, Category

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)