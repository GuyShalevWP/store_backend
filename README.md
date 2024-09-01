# Store - Django API

This is a Django-based API for "Store," an e-commerce platform implementing user authentication, product management, cart functionality, and order processing. It leverages Django Rest Framework (DRF) and JWT for secure API authentication.

## Features

-   User Authentication: Register, login, and manage user profiles.
-   Product Management: Staff users can manage products in the catalog.
-   Cart Management: Users can manage their shopping carts.
-   Order Management: Users can place orders, which move items from the cart to an order.

## Endpoints Overview

### Authentication

Login:
Endpoint: /api/login/
Method: POST
Description: User login using JWT. Provides access and refresh tokens.
Register:
Endpoint: /api/register/
Method: POST
Description: Register a new user. The role can be client, staff, or admin.

### User Profiles

UserProfileViewSet:

Endpoint: /api/user-profiles/
Methods: GET, PUT, PATCH
Description: Manage user profiles. Staff users can view all profiles, while regular users can only view their own profile.
PasswordChangeView:

Endpoint: /api/change-password/
Method: POST
Description: Allows authenticated users to change their password.

### Products

ProductViewSet:
Endpoint: /api/products/
Methods: GET, POST, PUT, PATCH, DELETE
Description: Allows staff users to manage products in the catalog.

### Cart

CartViewSet:

Endpoint: /api/carts/
Methods: GET, POST
Description: Manage the cart associated with the logged-in user.
CartItemViewSet:

Endpoint: /api/cart-items/
Methods: GET, POST, PUT, PATCH, DELETE
Description: Manage items within the user's cart.

### Orders

OrderViewSet:

Endpoint: /api/orders/
Methods: GET, POST, PUT, PATCH
Description: Manage orders placed by the user. Transfers cart items to an order upon creation.
OrderItemViewSet:

Endpoint: /api/order-items/
Methods: GET, POST, PUT, PATCH, DELETE
Description: Manage individual items within a user's order.
