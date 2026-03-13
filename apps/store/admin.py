from django.contrib import admin
from  .models import Products, Order, OrderItem, Cart, CartItem

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'created_at')
    search_fields = ('user__email',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'products', 'quantity')
    search_fields = ('order__user__email', 'products__name')
    list_filter = ('order__created_at',)
    ordering = ('-order__created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'products', 'quantity')
    search_fields = ('cart__user__email', 'products__name')