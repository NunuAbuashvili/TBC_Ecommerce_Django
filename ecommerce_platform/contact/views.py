from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def contact(request: HttpRequest) -> HttpResponse:
    """
    Render the contact page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'contact.html' template for the contact page.
    """
    return render(request, 'contact.html')
