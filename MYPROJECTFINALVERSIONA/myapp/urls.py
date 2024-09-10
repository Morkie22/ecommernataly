from django.urls import path
from . import views

urlpatterns = [
    # General views
    path('', views.index, name='index'),  # Home page displaying main products
    path('signup/', views.signup_view, name='signup'),  # User signup page
    path('login/', views.login_view, name='login'),  # User login page
    path('logout/', views.logout_view, name='logout'),  # User logout
    path('profile/', views.profile_view, name='profile'),  # User profile page

    # Product views
    path('products/', views.product_list_view, name='product_list'),  # List of products
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('product/create/', views.product_create_view, name='product_create'),  # Create a new product
    path('product/<int:pk>/update/', views.product_update_view, name='product_update'),  # Update an existing product
    path('product/delete/<int:pk>/', views.product_delete_view, name='product_delete'),

    # Cart views
    path('cart/', views.cart_view, name='cart'),  # Display the cart
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),  # Add an item to the cart
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),  # Remove an item from the cart
    path('update_cart/', views.update_cart_view, name='update_cart'),  # Update cart item quantities
    path('get_cart/', views.get_cart_view, name='get_cart'),  # Get cart data

    # Order and checkout views
    path('checkout/', views.checkout_view, name='checkout'),  # Checkout process
    path('place_order/', views.place_order_view, name='place_order'),  # Place an order
    path('order_confirmation/', views.order_confirmation_view, name='order_confirmation'),  # Order confirmation page
    path('is_logged_in/', views.is_logged_in_view, name='is_logged_in'),  # Check login status
]

