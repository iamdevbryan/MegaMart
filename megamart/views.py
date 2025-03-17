from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItem, Shop, Category
from .serializer import ProductSerializer, OrderSerializer, ShopSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer, RegisterSerializer

# Liste des produits
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Liste des boutiques
@api_view(['GET'])
def shop_list(request):
    shops = Shop.objects.all()
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data)


# Inscription
@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        Order.objects.create(user=user)  # Création automatique d'une commande vide
        return Response({
            "message": "Inscription réussie",
            "user": {"username": user.username, "email": user.email, "id": user.id}
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Connexion
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        
        # Vérifier si l'utilisateur a déjà une commande, sinon en créer une
        if not Order.objects.filter(user=user).exists():
            Order.objects.create(user=user)

        return Response({
            "message": "Connexion réussie",
            "user": {"username": user.username, "email": user.email, "id": user.id}
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Nom d'utilisateur ou mot de passe incorrect"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_order(request, user_id):
    try:
        order = Order.objects.get(user_id=user_id, validated=False)
        items = [{"id": item.id, "product": item.product.name, "quantity": item.quantity, "price": item.price} for item in order.order_items_set.all()]
        return Response({"order_id": order.id, "items": items, "total_price": order.get_total_price(), "total_quantity": order.get_total_quantity()})
    except Order.DoesNotExist:
        return Response({"error": "Commande non trouvée"}, status=404)


# Ajouter un produit à la commande
@api_view(['POST'])
def add_to_order(request, user_id):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    print(product_id, quantity)

    try:
        order = Order.objects.get(user_id=user_id, validated=False)
        product = Product.objects.get(id=product_id)

        # Vérifier si l'item existe déjà dans la commande
        item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={"quantity": quantity, "price": product.get_discounted_price()})
        if not created:
            item.quantity += int(quantity)
            item.save()

        return Response({"message": "Produit ajouté", "order_id": order.id, "success":True})
    except Order.DoesNotExist as e:
        print(e)
        return Response({"error": "Commande non trouvée"}, status=404)
    except Product.DoesNotExist as e:
        print(e)
        return Response({"error": "Produit non trouvé"}, status=404)

# Supprimer un item de la commande
@api_view(['DELETE'])
def remove_from_order(request, item_id):
    try:
        item = OrderItem.objects.get(id=item_id)
        item.delete()
        return Response({"message": "Item supprimé"})
    except OrderItem.DoesNotExist:
        return Response({"error": "Item non trouvé"}, status=404)

# Vider complètement la commande
@api_view(['DELETE'])
def clear_order(request, user_id):
    try:
        order = Order.objects.get(user_id=user_id, validated=False)
        order.clear_items()
        return Response({"message": "Commande vidée"})
    except Order.DoesNotExist:
        return Response({"error": "Commande non trouvée"}, status=404)
    
@api_view(['GET'])
def get_category(request, category_name):
    try:
        category = Category.objects.get(name=category_name)

        category_products = Product.objects.filter(categories=category)

        serializer = ProductSerializer(category_products, many=True)

        return Response(serializer.data)
    
    except Category.DoesNotExist:
        return Response({"message": "La catégorie n'existe pas"}, status=404)
    except Exception as e:
        print(e)
        return Response({"message": "Il y a une erreur"}, status=500)