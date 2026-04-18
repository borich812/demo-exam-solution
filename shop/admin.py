from django.contrib import admin
from .models import Category, CakeType, Manufacturer, Order, OrderItem, OrderStatus, PickupPoint, Product, Profile, Supplier

admin.site.register(Profile)
admin.site.register(Supplier)
admin.site.register(Manufacturer)
admin.site.register(CakeType)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(PickupPoint)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(OrderItem)
