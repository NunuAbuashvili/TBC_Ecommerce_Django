from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Tea, Category, Tag


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


def shop(request: HttpRequest) -> HttpResponse:
    """
    Display a paginated list of all available tea products in the shop.

    Retrieves and paginates the list of teas, optionally filtering by price range,
    tags, and sorting order (e.g., by rating, price, or creation date).
    Filters and sorting preferences are stored in the session. Common context data
    (categories, products, holiday products) is automatically included via the context processor.

    Args:
        request (HttpRequest): The HTTP request object, potentially containing POST data for filters.

    Returns:
        HttpResponse: The rendered 'shop.html' template with the paginated and optionally filtered tea products.
    """
    # TODO: სორტირება და გაფილტვრა ერთად არ მუშაობს (მაგალითად, თუ მინდა, რომ გაფილტრული პროდუქტები ფასის ზრდადობის მიხედვით დავალაგო).
    tags = Tag.objects.all()

    if request.method == 'POST':
        request.session['filter_price_range'] = request.POST.get('price_range')
        request.session['filter_tag_selected'] = request.POST.get('tag_selected')
        request.session['filter_sorting'] = request.POST.get('sorting')

    products = Tea.objects.select_related('category').prefetch_related('tags')

    price_range = request.session.get('filter_price_range')
    tag_selected = request.session.get('filter_tag_selected', None)
    sorting_option = request.session.get('filter_sorting', None)

    try:
        price_upper_limit = int(price_range) if price_range else 0
    except ValueError:
        price_upper_limit = 0

    if sorting_option == 'rating':
        order_option = '-rating'
    elif sorting_option == 'low_high':
        order_option ='price'
    elif sorting_option == 'high_low':
        order_option = '-price'
    elif sorting_option == 'date':
        order_option = '-created_at'
    else:
        order_option = 'name'

    if price_upper_limit > 1 and not tag_selected:
        filtered_products = products.filter(price__lte=price_upper_limit).order_by(order_option)
    elif price_upper_limit == 0 and tag_selected:
        filtered_products = products.filter(tags__name=tag_selected).order_by(order_option)
    elif price_upper_limit > 0 and tag_selected:
        filtered_products = products.filter(
            Q(tags__name=tag_selected) &
            Q(price__lte=price_upper_limit)
        ).order_by(order_option)
    else:
        filtered_products = products.order_by(order_option)

    paginator = Paginator(filtered_products, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'shop.html', context={'products': page_object, 'tags': tags})


def clear_filters(request: HttpRequest) -> HttpResponse:
    """
    Clear all applied filters (price range, tag selection, sorting) from the session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'shop' view after clearing session filters.
    """
    if request.method == 'POST':
        request.session.pop('filter_price_range', None)
        request.session.pop('filter_tag_selected', None)
        request.session.pop('filter_sorting', None)

    return redirect('store:shop')


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


def get_category(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Retrieve a specific category and show its title on the header.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The unique slug identifier for the category.

    Returns:
        HttpResponse: Rendered template with the category context.

    Raises:
        Http404: If the category with the given slug does not exist.
    """
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'single-page-header.html', context={'category': category})


def search(request: HttpRequest) -> HttpResponse:
    """
    Search for tea products based on user query.

    Performs a case-insensitive search across tea names, descriptions,
    and category names. Uses select_related to optimize database queries.

    Args:
        request (HttpRequest): The HTTP request object containing the search query
            in GET parameters.

    Returns:
        HttpResponse: Rendered template with search results.
    """
    if request.method == 'GET':
        inquiry = request.GET.get('searched')

        search_results = Tea.objects.select_related('category').filter(
            Q(name__icontains=inquiry) |
            Q(description__icontains=inquiry) |
            Q(category__name__icontains=inquiry)
        ).distinct().select_related('category')
    else:
        return render(request, 'search.html', {})

    return render(request, 'shop.html', context={'products': search_results})


def contact(request: HttpRequest) -> HttpResponse:
    """
    Render the contact page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'contact.html' template for the contact page.
    """
    return render(request, 'contact.html')
