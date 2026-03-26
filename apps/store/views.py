from django.shortcuts import get_object_or_404
from .models import Products, Order, OrderItem, Cart, CartItem
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema


class ProductListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def get(self, request):
        products = Products.objects.all()
        return Response(ProductSerializer(products, many=True).data, status=200)


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = CreateProductSerializer

    @swagger_auto_schema(request_body=CreateProductSerializer, responses={201: ProductSerializer})
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff or not request.user.is_active:
            return Response({"error": "Only active admins can create products"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class ProductDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(responses={200: ProductSerializer})
    def get(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        return Response(ProductSerializer(product).data)

    @swagger_auto_schema(request_body=CreateProductSerializer, responses={200: ProductSerializer})
    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        product = get_object_or_404(Products, pk=pk)
        serializer = CreateProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: "Deleted"})
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        product = get_object_or_404(Products, pk=pk)
        product.delete()
        return Response(status=204)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @swagger_auto_schema(responses={200: CartSerializer})
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    @swagger_auto_schema(request_body=CartItemSerializer, responses={201: CartItemSerializer})
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    @swagger_auto_schema(request_body=CartItemSerializer, responses={200: CartItemSerializer})
    def put(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)

        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: "Deleted"})
    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        item.delete()
        return Response(status=204)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    @swagger_auto_schema(request_body=CreateOrderSerializer, responses={201: OrderSerializer})
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.all()

        if not items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.create(
            user=request.user,
            product=items.first().products,
            quantity=1,
            total_price=0,
            payment_method_id=serializer.validated_data.get("payment_method"),
            delivery_service_id=serializer.validated_data.get("delivery_service"),
            delivery_address=serializer.validated_data.get("delivery_address"),
            delivery_postal_code=serializer.validated_data.get("delivery_postal_code"),
            delivery_city=serializer.validated_data.get("delivery_city"),
        )

        total = 0

        for item in items:
            if item.products.stock < item.quantity:
                return Response(
                    {"error": f"{item.products.name} is out of stock"},
                    status=400
                )

            OrderItem.objects.create(
                order=order,
                products=item.products,
                quantity=item.quantity
            )

            item.products.stock -= item.quantity
            item.products.save()

            total += item.products.price * item.quantity

        order.total_price = total
        order.save()

        items.delete()

        return Response(OrderSerializer(order).data, status=201)


class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)