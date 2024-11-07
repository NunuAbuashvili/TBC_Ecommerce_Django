from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from order.models import CartItem


class Command(BaseCommand):
    help = 'Shows top 3 most frequently added products across all shopping carts.'

    def handle(self, *args, **options):
        popular_items = (
            CartItem.objects
            .values('product__name')
            .annotate(cart_count=Count('product__name'))
            .order_by('-cart_count')[:3]
        )

        if not popular_items:
            self.stdout.write(self.style.WARNING('Could not find 3 popular products.'))
            return

        self.stdout.write(self.style.SUCCESS('Top 3 most popular items:'))
        for idx, item in enumerate(popular_items, 1):
            self.stdout.write(
                f"{idx}. {item['product__name']} - in {item['cart_count']} carts"
            )
