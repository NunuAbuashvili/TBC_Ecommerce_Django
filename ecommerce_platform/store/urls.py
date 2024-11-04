from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name='store'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category', cache_page(60 * 10)(views.TeaListView.as_view()), name='shop'),
    path('category/<slug:slug>/', cache_page(60 * 10)(views.TeaListView.as_view()), name='category_page'),
    path('search/', views.TeaListView.as_view(), name='search'),
    path('product/<slug:slug>/', views.TeaDetailView.as_view(), name='product_page'),
    path('contact/', views.send_email, name='contact'),
]
