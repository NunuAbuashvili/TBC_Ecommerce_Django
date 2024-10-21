from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from store.models import Tea


def cart(request: HttpRequest) -> HttpResponse:
    """
    Display the shopping cart for the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns
        HttpResponse: The rendered 'cart.html' template displaying the user's cart.
    """
    cart_items = Tea.objects.all()[:3]
    return render(request, 'cart.html', context={'cart_items': cart_items})


def checkout(request: HttpRequest) -> HttpResponse:
    """
    Display the checkout page for the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'checkout.html' template for user checkout.
    """
    cart_items = Tea.objects.all()[:3]
    return render(request, 'checkout.html', context={'cart_items': cart_items})
