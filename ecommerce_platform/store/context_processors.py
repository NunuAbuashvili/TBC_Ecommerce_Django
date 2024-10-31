from typing import Dict
from django.db.models import Count
from django.http import HttpRequest
from .models import Category, Tea
from order.models import Cart


def common_data(request: HttpRequest) -> Dict[str, object]:
    """
    Provide commonly used context data for categories, products, and holiday teas.

    This context processor is automatically called on every request to add categories,
    active products, and holiday-themed teas (e.g., 'Christmas Tea') to the context.

    Args:
        request (HttpRequest): The request object.

    Returns:
        Dict[str, object]: A dictionary of context variables.
    """
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(is_active=True)

    products = Tea.objects.select_related('category').filter(is_active=True)

    holiday_products = Tea.objects.filter(category__name='Christmas Tea').filter(is_active=True)

    cart = Cart(request)

    return {
        'categories': categories,
        'products': products,
        'holiday_products': holiday_products,
        'cart': cart,
    }


def cart_size(request: HttpRequest) -> Dict[str, int]:
    """
    Context processor that provides the cart size for the current user.

    Args:
        request (HttpRequest): The current HTTP request object

    Returns:
        Dict[str, int]: Dictionary containing the 'cart_length' key with
            the number of items in the user's cart. Returns 0 for
            unauthenticated users.
    """
    cart_length = 0

    if request.user.is_authenticated:
        cart = request.user.cart
        cart_length = sum(cart_item.quantity for cart_item in cart.items.all())

    return {'cart_length': cart_length}
