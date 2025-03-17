from rest_framework import serializers
from .models import Product, Order, OrderItem, Shop
from django.contrib.auth.models import User


# Sérializer Boutique
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name',]

# Sérializer Produit
class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id', 'shop_name', 'name', 'description', 'image', 'price', 'discount_percentage', 'discounted_price']

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()
    
    def get_shop_name(self, obj):
        return obj.shop.name

# Sérializer Item de commande
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'get_subtotal']

# Sérializer Commande
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items', 'total_price', 'total_quantity']

    def get_total_price(self, obj):
        return obj.get_total_price()
    
    def get_total_quantity(self, obj):
        return obj.get_total_quantity()
    


#Sérializer Utilisateur
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user