from django.contrib import admin
from .models import Product, Category, UserProfile

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Category)

