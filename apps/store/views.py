from django.shortcuts import render, get_object_or_404
from .models import Products, Order, OrderItem, Cart, CartItem
from .serializers import ProductsSerializer, OrderSerializer, CartSerializer, CartItemSerializer, OrderItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from drf_yasg.utils import swagger_auto_schema

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductsSerializer, responses={201: ProductsSerializer})
    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: ProductsSerializer})
    def get(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductsSerializer, responses={200: ProductsSerializer})
    def put(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        serializer = ProductsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "Deleted"})
    def delete(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: CartSerializer})
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CartItemSerializer, responses={201: CartItemSerializer})
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        data = request.data.copy()
        data["cart"] = cart.id

        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartItemView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CartItemSerializer, responses={200: CartItemSerializer})
    def put(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        serializer = CartItemSerializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "Deleted"})
    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCreateView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=OrderSerializer, responses={201: OrderSerializer})
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


