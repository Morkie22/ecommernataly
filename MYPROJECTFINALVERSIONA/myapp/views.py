from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from .models import Product
from .forms import ProductForm

# Utility Function
def admin_required(user):
    """Check if user is an admin."""
    return user.is_staff

# Utility Function for Cart Management
def update_cart_session(request, product_id, quantity):
    """Utility to update cart in session."""
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[product_id] = quantity
    elif product_id in cart:
        del cart[product_id]
    request.session['cart'] = cart
    return cart

# Public Views
def index(request):
    """Home Page / Index View."""
    return render(request, 'index.html')

def signup_view(request):
    """Signup View."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Signup successful!')
            return redirect('index')
        else:
            messages.error(request, 'Signup failed. Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'auth_templates/signup.html', {'form': form})  # Ensure the correct path to your templates

def login_view(request):
    """Login View."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid login details.')
    else:
        form = AuthenticationForm()
    
    # Correct the template path based on your directory structure
    return render(request, 'AUTH TEMPLATES/login.html', {'form': form})

def logout_view(request):
    """Logout View."""
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

@login_required
def profile_view(request):
    """Profile View."""
    return render(request, 'profile.html', {'user': request.user})

# Cart Views
def cart_view(request):
    """Cart View."""
    cart = request.session.get('cart', {})
    return render(request, 'cart.html', {'cart': cart})

def add_to_cart_view(request):
    """Add to Cart View."""
    product_id = request.POST.get('product_id')
    update_cart_session(request, product_id, 1)  # Add one item to cart
    messages.success(request, 'Product added to cart.')
    return redirect('product_list')

def remove_from_cart_view(request):
    """Remove from Cart View."""
    product_id = request.POST.get('product_id')
    update_cart_session(request, product_id, 0)  # Remove item from cart
    messages.success(request, 'Product removed from cart.')
    return redirect('cart')

def update_cart_view(request):
    """Update Cart View."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    update_cart_session(request, product_id, quantity)  # Update cart with given quantity
    messages.success(request, 'Cart updated successfully.')
    return redirect('cart')

def get_cart_view(request):
    """Get Cart View."""
    cart = request.session.get('cart', {})
    return JsonResponse({'cart': cart})

# Checkout and Order Views
def checkout_view(request):
    """Checkout View."""
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        products.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity
        })
        total_price += product.price * quantity
    
    if request.method == 'POST':
        request.session['order'] = {'products': products, 'total_price': total_price}
        return redirect('order_confirmation')

    return render(request, 'checkout.html', {'cart': products, 'total_price': total_price})

@login_required
def place_order_view(request):
    """Place Order View."""
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty. Add products to proceed.')
        return redirect('product_list')

    request.session['cart'] = {}  # Clear the cart after processing
    messages.success(request, 'Your order has been placed successfully!')
    return redirect('order_confirmation')

@login_required
def order_confirmation_view(request):
    """Order Confirmation View."""
    order = request.session.get('order', {})
    if not order:
        messages.error(request, 'No order found. Please try checking out again.')
        return redirect('cart')

    return render(request, 'order_confirmation.html', {
        'order_details': order['products'],
        'total_price': order['total_price']
    })

def is_logged_in_view(request):
    """Check if the user is logged in."""
    return JsonResponse({'is_logged_in': request.user.is_authenticated})

# Product Views for All Users
def product_list_view(request):
    """Product List View."""
    products = Product.objects.all()
    return render(request, 'productViews/product_list.html', {'products': products})

def product_detail_view(request, pk):
    """Product Detail View."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})

# Product Management Views (Admin Only)
@user_passes_test(admin_required)
def product_create_view(request):
    """Create Product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to create product. Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'productViews/product_form.html', {'form': form})

@user_passes_test(admin_required)
def product_update_view(request, pk):
    """Update Product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to update product. Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'productViews/product_form.html', {'form': form})

@user_passes_test(admin_required)
def product_delete_view(request, pk):
    """Delete Product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'productViews/product_confirm_delete.html', {'product': product})
