from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    path('guest/', views.guest_view, name='guest'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<str:pk>/edit/', views.product_update, name='product_update'),
    path('products/<str:pk>/delete/', views.product_delete, name='product_delete'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
]
