from rest_framework import serializers
from .models import Products, Order, OrderItem, Cart, CartItem, PaymentMethod, DeliveryService

class ProductsSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'desccription', 'price', 'stock', 'category', 'category_display', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
   

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_at', 'payment_method', 'delivery_service', 'items']

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'products', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

    