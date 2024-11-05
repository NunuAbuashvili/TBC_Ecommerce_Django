from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from decimal import Decimal

from store.models import Tea
from .models import Cart, CartItem


class CartView(LoginRequiredMixin, TemplateView):
    """ Display the shopping cart for the user. """
    template_name = 'cart.html'
    login_url = "/accounts/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        context['cart'] = cart
        context['cart_items'] = cart.items.all().select_related('product')
        context['subtotal'] = cart.total_price
        # Checkout-ის გვერდზე ჩამოთვლილია მიწოდების სამი მეთოდი, თუმცა ფუნქციონალი ჯერჯერობით არ მუშაობს.
        context['shipping'] = Decimal('5.00')
        context['total'] = cart.total_price + context['shipping']
        return context


class AddToCartView(LoginRequiredMixin, View):
    """
    Add a product to the user's cart or update its quantity if it already exists.
    """
    login_url = "/accounts/login"

    def get(self, request: HttpRequest, product_id: int) -> HttpResponse:
        """
        Handle GET requests that occur after login redirect.
        """
        # იმ შემთხვევაში, თუ არაავტორიზებული მომხმარებელი ცდილობს პროდუქტის კალათაში დამატებას,
        # სესიაში ვინახავ პროდუქტის აიდისა და რაოდენობას, ხოლო მომხმარებელს წარმატებული ავტორიზაციის შემდეგ
        # გადავამისამართებ კალათის გვერდზე. სესიაში შენახულ მონაცემებს იყენებს CustomLoginView accounts app-ში.
        request.session['pending_cart_add'] = {
            'product_id': product_id,
            'quantity_to_add': request.POST.get('quantity_to_add', 1)
        }

        return redirect(f'{self.login_url}?next={reverse("order:cart")}')

    def post(self, request: HttpRequest, product_id: int) -> HttpResponse:
        """
        Handle POST requests for adding items to cart.
        """
        product = get_object_or_404(Tea, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # პროდუქტის დეტალურ გვერდზე მომხმარებელს შეუძლია აირჩიოს,
        # თუ რამდენი პროდუქტის დამატება სურს კალათაში.
        quantity_to_add = request.POST.get('quantity_to_add')

        if quantity_to_add is not None:
            quantity_to_add = int(quantity_to_add)

            # თუ პროდუქტი უკვე იყო კალათაში დამატებული
            if not created:
                # მითითებული რაოდენობის დამატება შესაძლებელია მხოლოდ იმ შემთხვევაში,
                # თუ მარაგში საკმარისი რაოდენობაა.
                if (cart_item.quantity + quantity_to_add) <= product.stock_quantity:
                    cart_item.quantity += quantity_to_add
                else:
                    available_quantity = product.stock_quantity - cart_item.quantity
                    if available_quantity > 0:
                        messages.warning(
                            request, f"Only {available_quantity} item(s) available in stock."
                        )
                    else:
                        messages.warning(request, 'Sorry, the item is out of stock.')
                    return redirect(request.META['HTTP_REFERER'])
            # თუ პროდუქტს პირველად ვამატებთ კალათაში
            else:
                if cart_item.quantity <= product.stock_quantity:
                    cart_item.quantity = quantity_to_add
                else:
                    messages.warning(
                        self.request, f"Only {product.stock_quantity} item(s) available in stock."
                    )

            cart_item.save()

        return redirect('order:cart')

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to handle unauthorized users trying to add to cart.
        """
        if not request.user.is_authenticated:
            return self.get(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class UpdateCartView(LoginRequiredMixin, UpdateView):
    """ Update the quantity of an item in the cart. """
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id)

        current_quantity = cart_item.quantity
        stock_quantity = cart_item.product.stock_quantity

        if action == 'increase':
            if current_quantity < stock_quantity and current_quantity + 1 <= stock_quantity:
                cart_item.quantity += 1
                cart_item.save()
        elif action == 'decrease':
            if current_quantity == 1:
                cart_item.delete()
            else:
                cart_item.quantity -= 1
                cart_item.save()

        return redirect('order:cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    """ Remove an item from the cart. """
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

        return redirect('order:cart')


class CheckoutView(LoginRequiredMixin, TemplateView):
    """ Display the checkout page for the user. """
    template_name = 'checkout.html'
    login_url = "/accounts/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        context['cart'] = cart
        context['cart_items'] = cart.items.all().select_related('product')
        context['subtotal'] = cart.total_price
        context['shipping'] = Decimal('5.00')
        context['total'] = cart.total_price + 5
        return context
