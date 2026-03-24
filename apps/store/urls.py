from django.urls import path
from .views import (
    ProductCreateView,
    ProductDetailView,
    CartView,
    AddToCartView,
    UpdateCartItemView,
    OrderCreateView,
    UserOrdersView,
    ProductListView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path("products/create/", ProductCreateView.as_view(), name="create-product"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),

    path("cart/", CartView.as_view(), name="view-cart"),
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/item/<int:pk>/", UpdateCartItemView.as_view(), name="update-cart-item"),

    path("orders/create/", OrderCreateView.as_view(), name="create-order"),
    path("orders/", UserOrdersView.as_view(), name="user-orders"),
]