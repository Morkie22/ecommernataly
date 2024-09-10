
# myproject/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from myapp import views  # Ensure you import the views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),  # Correctly route to login_view
    path('logout/', views.logout_view, name='logout'),  # Correctly route to logout_view
    path('signup/', views.signup_view, name='signup'),  # Correctly route to signup_view
    path('profile/', views.profile_view, name='profile'),  # Correctly route to profile_view
    path('cart/', views.cart_view, name='cart'),  # Route to cart view
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),  # Route to add to cart view
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),  # Route to remove from cart view
    path('update_cart/', views.update_cart_view, name='update_cart'),  # Route to update cart view
    path('checkout/', views.checkout_view, name='checkout'),  # Route to checkout view
    path('place_order/', views.place_order_view, name='place_order'),  # Route to place order view
    path('order_confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),  # Route to order confirmation view
    path('products/', views.product_list_view, name='product_list'),  # Route to product list view
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),  # Route to product detail view
    path('product/create/', views.product_create_view, name='product_create'),  # Route to create product view
    path('product/<int:pk>/update/', views.product_update_view, name='product_update'),  # Route to update product view
    path('product/<int:pk>/delete/', views.product_delete_view, name='product_delete'),  # Route to delete product view
    path('', include('myapp.urls')),  # Include other URLs from your app
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
