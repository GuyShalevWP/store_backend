from django.db import models
from django.contrib.auth.models import User

# categories model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
# user model
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        # Capitalize the first letter of the role before saving
        self.role = self.role.capitalize()
        super(UserProfile, self).save(*args, **kwargs)

# products model
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_img = models.ImageField(
        upload_to='products/', 
        null=True, 
        blank=True, 
        default='products/default_image/img_not_found.webp'
    )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    # created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    from django.db import models

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    
    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='cart_items')
    amount = models.PositiveIntegerField(default=1)
    sum_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} x {self.product.title} in {self.cart.user.username}'s cart"

# order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    arrival_date = models.DateTimeField(null=True, blank=True)
    is_arrived = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} on {self.order_date.strftime('%Y-%m-%d')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
    amount = models.PositiveIntegerField(default=1)
    sum_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} x {self.product.title} (Order {self.order.id})"