from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Tea, Category


def shop(request: HttpRequest) -> HttpResponse:
    """
    Display a paginated list of all available tea products in the shop.

    Retrieves and paginates the list of teas, ordering them by name.
    Common context data (categories, products, holiday products) is automatically
    included via the context processor.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered 'shop.html' template with the paginated tea products.
    """
    products = Tea.objects.order_by('name')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'shop.html', context={'page_object': page_object})


def product_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Display details of a specific tea product, including related products from the same category.

    Fetches a tea product by its slug and displays its details, along with related products
    in the same category. If the product is not found, render a 404 page.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the tea product to retrieve.

    Returns:
        HttpResponse: The rendered 'shop-detail.html' template with product details.
        HttpResponse: A rendered '404.html' template if the product is not found.
    """
    try:
        product = Tea.objects.select_related('category').get(slug=slug)
    except Tea.DoesNotExist:
        return render(request, '404.html', status=404)

    related_products = Tea.objects.filter(category=product.category).exclude(id=product.id)

    context = {
        'product': product,
        'category': product.category,
        'related_products': related_products,
    }

    return render(request, 'shop-detail.html', context)


def category_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Display a paginated list of products in a specific category.

    Fetches a category by its slug and displays all products within that category,
    paginating them. If the category is not found, renders a 404 page.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the category to retrieve.

    Returns:
        HttpResponse: The rendered 'category-category.html' template with category products.
        HttpResponse: A rendered '404.html' template if the category is not found.
    """
    try:
        category = Category.objects.prefetch_related('products').get(slug=slug)
    except Category.DoesNotExist:
        return render(request, '404.html', status=404)

    category_products = category.products.all().order_by('name')

    paginator = Paginator(category_products, 3)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {
        'category': category,
        'category_products': category_products,
        'page_object': page_object,
    }

    return render(request, 'category-detail.html', context)
