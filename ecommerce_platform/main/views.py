from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from store.models import Tea


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page with featured products.

    This view fetches a selection of tea products to display on the home page,
    including the top-rated products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'home.html' template with the selected products.
    """
    products = Tea.objects.select_related('category')[:8]
    products_with_highest_rating = Tea.objects.filter(rating__gte=5)[:6]

    context = {
        'products': products,
        'products_with_highest_rating': products_with_highest_rating
    }

    return render(request,'home.html', context)
