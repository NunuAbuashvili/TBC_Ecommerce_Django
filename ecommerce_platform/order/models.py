from django.db import models
from accounts.models import CustomUser
from store.models import Tea
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import Any


class Cart(models.Model):
    """
    Represents a shopping cart for a user.

    Attributes:
        user (CustomUser): The user who owns the cart.
        created_at (datetime): The date and time when the cart was created.
        updated_at (datetime): The date and time when the cart was last updated.
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self) -> float:
        """ Calculate total price of all items in the cart. """
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self) -> int:
        """ Calculate total number of items in the cart. """
        return self.items.count()

    def clear(self) -> None:
        """ Remove all items from the cart. """
        self.items.all().delete()

    def __str__(self):
        """ Return the string representation of the cart. """
        return f"{self.user.username}'s cart"

    class Meta:
        verbose_name = "User's Cart"
        verbose_name_plural = "Users' Carts"


@receiver(post_save, sender=CustomUser)
def create_user_cart(sender: Any, instance: CustomUser, created: bool, **kwargs: Any) -> None:
    """
    Create a cart for the user when a new CustomUser is created.

    Args:
        sender (Any): The sender of the signal.
        instance (CustomUser): The user instance being created.
        created (bool): Flag indicating if the instance was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Cart.objects.create(user=instance)


class CartItem(models.Model):
    """
    Represents an item in the shopping cart.

    Attributes:
        cart (Cart): The cart that this item belongs to.
        product (Tea): The product being purchased.
        quantity (int): The quantity of the product being purchased.
        added_at (datetime): The date and time when the item was added to the cart.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Tea, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        """ Calculate price for this item. """
        return self.quantity * self.product.price

    def __str__(self):
        """ Return the string representation of the cart item. """
        return f'{self.quantity} of {self.product.name}'

    class Meta:
        unique_together = ('cart', 'product')
