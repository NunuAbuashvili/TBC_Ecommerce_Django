from typing import Dict
from django.db.models import Count
from django.http import HttpRequest
from .models import Category, Tea


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

    return {
        'categories': categories,
        'products': products,
        'holiday_products': holiday_products,
    }
