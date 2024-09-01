from django.utils import timezone
from django.forms import ValidationError
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied
from .models import CartItem, Order, OrderItem, Product, UserProfile, Cart
from .serializer import CartItemSerializer, OrderItemSerializer, OrderSerializer, PasswordChangeSerializer, ProductSerializer, MyTokenObtainPairSerializer, CartSerializer, UserProfileSerializer
from .permissions import IsStaffUser, IsOwner


@api_view(['GET'])
def index(req):
    return Response('hello')

# login
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
    )
    
    # Assign role
    role = request.data.get('role', 'client')  # Default role is 'client'
    if role not in ['client', 'staff', 'admin']:
        return Response({"error": "Invalid role provided."}, status=400)

    # Create the user profile with the role
    UserProfile.objects.create(user=user, role=role)
    user.is_active = True
    user.is_staff = (role in ['staff', 'admin'])  # Automatically set is_staff based on role
    user.save()

    return Response("New user created successfully.")

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Use the detailed serializer for all actions
        return UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()  # Staff can see all profiles
        return User.objects.filter(user=user)  # Regular users can only see their own profile

    def perform_update(self, serializer):
        user = self.request.user
        user_profile = self.get_object()

        # Check if the user is allowed to update this profile
        if user != user_profile.user and not user.is_staff:
            raise PermissionDenied("You do not have permission to update this profile.")

        # Check if the user is trying to change the role
        if 'role' in serializer.validated_data and user_profile.role != serializer.validated_data['role']:
            if user_profile.user == user:
                raise PermissionDenied("You cannot change your own role.")
            if not (user.is_staff and user.userprofile.role == 'Admin'):
                raise PermissionDenied("Only admins can change the role of other users.")
        
        serializer.save()

    def perform_destroy(self, instance):
        raise PermissionDenied("Deletion is not allowed.")

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deletion is not allowed."}, status=status.HTTP_403_FORBIDDEN)
    
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffUser]

# cart
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only the cart for the current user
        # Assuming each user has only one active cart
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the cart with the logged-in user
        # Since each user should have only one cart, you might want to ensure this
        if not Cart.objects.filter(user=self.request.user).exists():
            serializer.save(user=self.request.user)
        else:
            raise ValidationError("A cart already exists for this user.")
        
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Filter to only show items in the cart belonging to the current user
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        # Automatically associate the cart item with the user's cart
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)

# orders
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only the orders that belong to the current user
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the order with the logged-in user and transfer cart items
        user = self.request.user
        cart = Cart.objects.get(user=user)

        # Create the order
        order = serializer.save(user=user)

        # Transfer cart items to order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.amount,
                sum_price=cart_item.sum_price
            )

        # Delete the cart after the order has been submitted
        cart.items.all().delete()
        cart.delete()

        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        # Get the order instance being updated
        order = self.get_object()

        # Prevent updates if the order is inactive
        if not order.is_active:
            raise ValidationError("This order is inactive and cannot be updated.")

        # Check if any restricted fields are being changed
        validated_data = serializer.validated_data

        # Prevent changes to certain fields
        restricted_fields = ['amount', 'product', 'order_date', 'sum_price']
        for field in restricted_fields:
            if field in validated_data:
                raise ValidationError(f"Cannot update the field '{field}'.")

        # Update the order instance
        order = serializer.save()

        # Set the arrival date if the order is marked as arrived and no arrival date is set
        if order.is_arrived and order.arrival_date is None:
            order.arrival_date = timezone.now()
            order.save()
    
class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Filter to only show items in orders belonging to the current user
        return OrderItem.objects.filter(order__user=self.request.user)