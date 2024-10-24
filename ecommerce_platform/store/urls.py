from django.urls import path
from . import views

app_name='store'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.shop, name='shop'),
    path('category/<slug:slug>/', views.category_detail_view, name='category_page'),
    path('search/', views.search, name='search'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_page'),
    path('contact/', views.contact, name='contact'),
]
