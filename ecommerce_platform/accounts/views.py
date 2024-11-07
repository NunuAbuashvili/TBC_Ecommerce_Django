from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

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


    password_error = []
    password_errors = form.errors.get('password2', [])
    for error in password_errors:
        if 'similar to' in error or 'გავს' in error:
            password_error.append('Similarity Error')
        elif 'short' in error or 'მოკლე' in error:
            password_error.append('Short Password Error')
        elif 'common' in error or 'ხშირად' in error:
            password_error.append('Common Password Error')
        elif 'numeric' in error or 'ციფრებისგან' in error:
            password_error.append('Numeric Password Error')
    return render(request, 'register.html', {"form": form, "password_error": password_error})


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
                cart, cart_created = Cart.objects.get_or_create(user=self.request.user)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

                if not created:
                    if (cart_item.quantity + quantity_to_add) <= cart_item.product.stock_quantity:
                        cart_item.quantity += quantity_to_add
                        cart_item.save()
                    else:
                        available_quantity = product.stock_quantity - cart_item.quantity
                        if available_quantity > 0:
                            messages.warning(
                                self.request,
                                _('Only %(quantity)s item(s) available in stock.')
                                % {'quantity': available_quantity},
                            )
                        else:
                            messages.warning(
                                self.request,
                                _('Sorry, the item is out of stock.')
                            )
                        return redirect(request.META['HTTP_REFERER'])
                else:
                    if quantity_to_add <= product.stock_quantity:
                        cart_item.quantity = quantity_to_add
                        cart_item.save()
                    else:
                        messages.warning(
                            self.request,
                            _('Only %(quantity)s item(s) available in stock.')
                            % {'quantity': product.stock_quantity},
                        )

            except Tea.DoesNotExist:
                messages.error(
                    self.request,
                    _('Product not found.')
                )

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
