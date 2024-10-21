from django.db.models import Count
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import Tea, Category


@admin.register(Tea)
class ProductAdmin(admin.ModelAdmin):
    """ Admin configuration for Tea model. """
    list_display = ('name', 'category', 'place_of_origin', 'price', 'stock_quantity', 'rating')
    list_filter = ('rating', 'place_of_origin', 'is_active', 'contains_caffeine')
    search_fields = ('name', 'category__name')
    search_help_text = 'Search by product name or category'
    list_editable = ('stock_quantity', 'price')
    ordering = ('stock_quantity',)
    save_on_top = True
    list_per_page = 10
    show_full_result_count = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Admin configuration for Category model. """
    list_display = ('name', 'is_active', 'number_of_products')
    search_fields = ('name',)
    search_help_text = 'Search by category name'
    ordering = ('name',)
    list_select_related = True
    save_on_top = True
    list_per_page = 10
    show_full_result_count = False

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """
        Enhance the base queryset with product counts for categories.

        This method overrides the base queryset to include an annotation
        that counts the number of products in each category.

        Args:
            request: The HTTP request object.

        Returns:
            QuerySet: The enhanced queryset with an additional 'product_count'
                      annotation for each category.
        """
        queryset = super().get_queryset(request)
        return queryset.annotate(product_count=Count('products', distinct=True))

    @admin.display(description='Number of products')
    def number_of_products(self, instance: Category) -> int:
        """
        Get the number of products directly in this category.

        Args:
            instance: The Category instance.

        Returns:
            int: Number of products in this category.
        """
        return instance.product_count
