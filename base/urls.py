
from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cartitem')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'order-items', views.OrderItemViewSet, basename='orderitem')
router.register(r'user', views.UserProfileViewSet, basename='userprofile')


urlpatterns = [
    path('', include(router.urls)),
    path('', views.index),
    path('register/', views.register),
    path('login/', views.LoginView.as_view()),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),

]
