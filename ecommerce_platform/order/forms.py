from django import forms
from store.models import Tea

class CartAddProductForm(forms.Form):
    """
    Form for adding products to the cart with quantity validation against stock levels.

    Attributes:
        quantity: IntegerField for specifying how many items to add to cart.
        product: Tea instance to validate against.
    """
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantity"
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with a product instance for stock validation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.product = kwargs.pop('product')
        super().__init__(*args, **kwargs)

    def clean_quantity(self) -> int:
        """
        Validate that the requested quantity doesn't exceed available stock.

        Returns:
            int: The validated quantity.

        Raises:
            ValidationError: If quantity exceeds available stock.
        """
        quantity = self.cleaned_data['quantity']
        if quantity > self.product.stock_quantity:
            raise forms.ValidationError(
                f"Only {self.product.stock_quantity} items are available."
            )
        return quantity


class CartQuantityForm(forms.Form):
    """
    Form for updating quantities of items already in the cart.

    Attributes:
        quantity: IntegerField for specifying the new quantity.
        item_id: Hidden field storing the cart item ID.
    """
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm text-center border-0',
                'style': 'width: 50px;'
            }
        )
    )
    item_id = forms.IntegerField(widget=forms.HiddenInput())

    #TODO: უნდა დავამატო შემოწმება, განახლების შემდეგ რაოდენობა ხომ არ გადააჭარბებს მარაგში არსებულ რაოდენობას.