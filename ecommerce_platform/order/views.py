from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from store.models import Tea
from .models import Cart, CartItem
from .forms import CartAddProductForm, CartQuantityForm


def cart_summary(request: HttpRequest) -> HttpResponse:
    """
    Display the shopping cart for the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns
        HttpResponse: The rendered 'cart.html' template displaying the user's cart.
    """
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_items = [{
            'id': item.id,
            'product_id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'subtotal': item.subtotal,
            'image': item.product.image,
            'max_quantity': item.product.stock_quantity
        } for item in cart.items.all().select_related('product')]

        subtotal = cart.total_price
        shipping = Decimal('5.00')
        total = subtotal + shipping
    else:
        messages.warning(request, "Please log in to view your cart.")
        return redirect('store:home')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }

    return render(request, 'cart.html', context)


def add_to_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Add a product to the user's cart or update its quantity if it already exists.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponse: Redirect to either the cart page or the previous page.
    """
    product = get_object_or_404(Tea, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if request.method == "POST":
        form = CartAddProductForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity

            cart_item.save()
        else:
            messages.warning(request, form.errors['quantity'][0])
            return redirect(request.META['HTTP_REFERER'])

    return redirect('order:cart')


@login_required
def update_cart_item(request: HttpRequest) -> HttpResponse:
    """
    Update the quantity of an item in the cart.

    Args:
        request(HttpRequest): The HTTP request object containing:
            - item_id: ID of the cart item to update.
            - action: 'increase' or 'decrease' or None.
            - quantity: New quantity value (for direct updates).

    Returns:
        HttpResponse: Redirect to the cart page.
    """
    # TODO: პლიუსზე ან მინუსზე დაჭერის შემდეგ გვერდი განახლდება, რის შედეგადაც იკარგება ინფორმაცია, ამიტომ ფუნქცია სწორად არ მუშაობს.
    # TODO: შემთხვევა, როდესაც პროდუქტის რაოდენობა არის ერთი და ვაწვები მინუსს, შესაბამისად, საერთოდ უნდა წაიშალოს კალათიდან.
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        try:
            cart_item = CartItem.objects.get(id=item_id)

            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                quantity = int(request.POST.get('quantity', 1))
                if quantity >= 1:
                    cart_item.quantity = quantity

            cart_item.save()

        except (CartItem.DoesNotExist, ValueError):
            pass

    return redirect('order:cart')


@login_required
def remove_from_cart(request: HttpRequest) -> HttpResponse:
    """
    Remove an item from the cart completely.

    Args:
        request (HttpRequest): The HTTP request object containing:
            - item_id: ID of the cart item to remove.

    Returns:
        HttpResponse: Redirect to the cart page.
    """
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

        return redirect('order:cart')


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
