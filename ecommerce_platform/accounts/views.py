from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from store.models import Tea
from order.models import Cart, CartItem


def register(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration.

    Args:
        request: The HTTP request object.

    Returns
        HttpResponse: Redirect to login page on success or render registration form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {"form": form})


class CustomLoginView(LoginView):
    """
    Extends Django's LoginView to handle user login.
    Also handles pending cart operations after login.
    """
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form: CustomAuthenticationForm) -> HttpResponse:
        """
        Handle successful login and process any pending cart operations.

        Args:
            form: The validated authentication form.

        Returns:
            HttpResponse: Redirect response after processing login and cart operations.
        """
        # იმ შემთხვევაში, თუ არაავტორიზებულმა მომხმარებელმა სცადა პროდუქტის კალათაში დამატება,
        # ეს ინფორმაცია ინახება სესიაში 'pending_cart_add' ლექსიკონის სახით (product_id, quantity_to_add),
        # წარმატებული ავტორიზაციის შემდეგ პროდუქტი მითითებული რაოდენობით ავტომატურად აისახება კალათაში.
        response = super().form_valid(form)
        pending_cart_add = self.request.session.pop('pending_cart_add', None)

        if pending_cart_add:
            product_id = pending_cart_add.get('product_id')
            quantity_to_add = pending_cart_add.get('quantity_to_add', 1)

            if quantity_to_add is not None:
                quantity_to_add = int(quantity_to_add)

            try:
                product = get_object_or_404(Tea, id=product_id)
                cart, _ = Cart.objects.get_or_create(user=self.request.user)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

                if not created:
                    if (cart_item.quantity + quantity_to_add) <= cart_item.product.stock_quantity:
                        cart_item.quantity += quantity_to_add
                        cart_item.save()
                    else:
                        available_quantity = product.stock_quantity - cart_item.quantity
                        if available_quantity > 0:
                            messages.warning(self.request, f"Only {available_quantity} item(s) available in stock.")
                        else:
                            messages.warning(self.request, 'Sorry, the item is out of stock.')
                        return redirect(request.META['HTTP_REFERER'])
                else:
                    if quantity_to_add <= product.stock_quantity:
                        cart_item.quantity = quantity_to_add
                        cart_item.save()
                    else:
                        messages.warning(self.request, f"Only {product.stock_quantity} item(s) available in stock.")

            except Tea.DoesNotExist:
                messages.error(self.request, 'Product not found.')

        return response


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    """
    Handle user logout.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Render the logout page.
    """
    logout(request)
    return render(request, 'logout.html')
