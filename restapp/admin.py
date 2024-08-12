from django.contrib import admin
from .models import Product, Review, UserCart, CartItem,ProductQuantity,Order

admin.site.register(Product)
admin.site.register(ProductQuantity)
admin.site.register(Review)
admin.site.register(UserCart)
admin.site.register(CartItem)
admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(DoctorPermission)