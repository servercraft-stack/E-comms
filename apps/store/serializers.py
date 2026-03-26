from rest_framework import serializers
from .models import Products, Order, OrderItem, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Products
        fields = "__all__"

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'image', 'category', 'stock']

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'products', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='products', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class CreateOrderSerializer(serializers.Serializer):
    payment_method = serializers.IntegerField(required=False)
    delivery_service = serializers.IntegerField(required=False)
    delivery_address = serializers.CharField(required=False)
    delivery_postal_code = serializers.CharField(required=False)
    delivery_city = serializers.CharField(required=False)