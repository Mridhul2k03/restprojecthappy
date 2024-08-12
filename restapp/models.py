from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q

class Product(models.Model):
    permission_options = (
        ('permission required', 'permission required'),
        ('permission not required', 'permission not required'),
    )
    permission = models.CharField(max_length=255, choices=permission_options)
    name = models.CharField(max_length=255)
    subname = models.CharField(max_length=255)
    incrediants = models.TextField()
    description = models.TextField()
    consern = models.TextField()
    key_benefits = models.JSONField()
    how_to_use = models.JSONField()
    precautions = models.JSONField()
    faqs = models.JSONField()
    status = models.BooleanField(default=True)
    added_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    use_for = models.CharField(max_length=100)
    use_with = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} Review by {self.user.username}'

class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Cart for {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.ForeignKey(ProductQuantity, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.cart.user.username} - {self.quantity}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.ForeignKey(ProductQuantity, on_delete=models.CASCADE,related_name='quandity')
    # total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.ForeignKey(ProductQuantity,on_delete=models.CASCADE,related_name='total_price')
    created_at = models.DateTimeField(auto_now_add=True)
    status_options=(
        ('pending', 'pending'),
        ('shipped', 'shipped'),
        ('out for delivery', 'out for delivery'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),
    )
    order_status = models.CharField(max_length=20, choices=status_options, default='pending')
    permmision_choices =(
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    ) 
    permission = models.CharField(max_length=20, choices=permmision_choices, default='pending')
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
    
    

    
class DoctorsPersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    phonenumber = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return self.name

class DoctorPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Order, on_delete=models.CASCADE)
    permission= models.ForeignKey(Product, on_delete=models.CASCADE)












# class OrderItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
#     Product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quntity = models.ForeignKey(ProductQuantity, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     status_options=(
#         ('pending', 'pending'),
#         ('shipped', 'shipped'),
#         ('out for delivery', 'out for delivery'),
#         ('delivered', 'delivered'),
#         ('cancelled', 'cancelled'),
#     )
#     order_status = models.CharField(max_length=20, choices=status_options, default='pending')
#     permmision_choices =(
#         ('pending', 'pending'),
#         ('accepted', 'accepted'),
#         ('rejected', 'rejected'),
#     ) 
#     permission = models.CharField(max_length=20, choices=permmision_choices, default='pending')
    

    # def __str__(self):
    #     return f'{self.order.user.username} - {self.Product.name}'