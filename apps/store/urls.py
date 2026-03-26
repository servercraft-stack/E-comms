from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/create/', ProductCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),

    path('cart/', CartView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
    path('cart/item/<int:pk>/', UpdateCartItemView.as_view()),

    path('orders/create/', OrderCreateView.as_view()),
    path('orders/', UserOrdersView.as_view()),
]