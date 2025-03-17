from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


# Modèle Catégorie
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Modèle Boutique
class Shop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Modèle Produit
class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")  # Lien avec la boutique
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField(default=0.0)  # Pourcentage de réduction
    categories = models.ManyToManyField(Category, blank=True)  # Lien avec les catégories


    def get_discounted_price(self):
        discount_decimal = Decimal(self.discount_percentage)
        return round(self.price * (Decimal(1) - discount_decimal / Decimal(100)), 2)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.categories.count() > 3:
            raise ValueError("Un produit ne peut pas avoir plus de 3 catégories.")


    def __str__(self):
        return self.name

# Modèle Commande
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) 
    validated = models.BooleanField(default=False)  

    def clear_items(self):
        self.items.clear()  

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.order_items_set.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.order_items_set.all())


# Modèle Item de commande
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0) 


    def get_subtotal(self):
        return self.product.get_discounted_price() * self.quantity