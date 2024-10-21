from django.urls import path
from . import views

app_name='store'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('<slug:slug>/', views.category_detail_view, name='category_page'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_page'),
]