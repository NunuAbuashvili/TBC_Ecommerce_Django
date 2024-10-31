from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Tea, Category, Tag


class HomeView(TemplateView):
    """
    Render the home page with featured products.

    This view fetches a selection of tea products to display on the home page,
    including the top-rated products.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # მთავარ გვერდზე მხოლოდ 8 შემთხვევითი პროდუქტი და 6 ყველაზე მაღალი შეფასების მქონე პროდუქტი ჩანს
        context['products'] = Tea.objects.select_related('category')[:8]
        context['products_with_highest_rating'] = Tea.objects.filter(rating__gte=5)[:6]
        return context


class TeaDetailView(DetailView):
    """ Display details of a specific tea product. """
    queryset = Tea.objects.select_related('category')
    template_name = 'shop-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ყველა დეტალური გვერდის ბოლოში არის სექცია, სადაც ნაჩვენებია იმავე კატეგორიის სხვა პროდუქტები
        category = self.object.category
        context['related_products'] = (
            self.queryset
            .filter(category=category)
            .exclude(id=self.object.id)
        )
        return context


class TeaListView(ListView):
    """
    Display a paginated list of all available tea products in the shop.

    Retrieves and paginates the list of teas, optionally filtering by price range,
    tags, and sorting order (e.g., by rating, price, or creation date).
    """
    model = Tea
    template_name = 'shop.html'
    context_object_name = 'product_list'
    ordering = 'name'
    paginate_by = 6

    def get_queryset(self):
        # ფასის და Tag-ის ფილტრი ერთად მუშაობს, რომელიმე Tag-ის არჩევის შემთხვევაში ფასიც 0-ზე მეტი უნდა მოინიშნოს.
        queryset = Tea.objects.select_related('category').prefetch_related('tags')
        category_slug = self.kwargs.get('slug')

        # GET-ის პარამეტრები პროდუქტების გასაფილტრად
        price_upper_limit = self.request.GET.get('price_range')
        tag_selected = self.request.GET.get('tag_selected')
        ordering = self.request.GET.get('ordering')
        search_query = self.request.GET.get('searched')

        # GET-ის პარამეტრების მიხედვით განახლებული queryset
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if price_upper_limit:
            queryset = queryset.filter(price__lte=price_upper_limit)

        if tag_selected:
            queryset = queryset.filter(tags__name=tag_selected)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        ordering_options = {
            'name': 'name',
            'rating': '-rating',
            'low_high': 'price',
            'high_low': '-price',
            'date': '-created_att'
        }

        if ordering in ordering_options:
            queryset = queryset.order_by(ordering_options[ordering])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # კატეგორიების ჩამონათვალში თითოეული კატეგორიის გვერდით
        # ფრჩხილებში მოცემულია იმ კატეგორიაში არსებული პროდუქტების რაოდენობა.
        context['categories'] = Category.objects.prefetch_related('products').annotate(
            product_count=Count('products')
        )
        context['tags'] = Tag.objects.all()
        context['current_category'] = self.kwargs.get('slug', '')

        try:
            # კატეგორია გადაეცემა Header-ს (Home / Shop / არჩეული კატეგორია)
            context['current_category_instance'] = Category.objects.get(
                slug=self.kwargs.get('slug')
            ) if self.kwargs.get('slug') else None
        except Category.DoesNotExist:
            context['current_category_instance'] = None

        context['current_price_upper_limit'] = self.request.GET.get('price_range', 0)
        context['current_tag'] = self.request.GET.get('tag_selected', '')
        context['current_ordering'] = self.request.GET.get('ordering', 'name')
        context['search_query'] = self.request.GET.get('searched', '')

        return context


class ContactFormView(TemplateView):
    """ Render the contact page. """
    # რადგან ჯერჯერობით ფუნქციონალი არ მაქვს შემუშავებული, ამიტომ TemplateView დავტოვე, მოგვიანებით გადავაკეთებ.
    template_name = 'contact.html'
