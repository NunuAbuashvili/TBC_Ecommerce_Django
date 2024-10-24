from django.urls import path
from . import views

app_name='order'

urlpatterns = [
    path('cart/', views.cart_summary, name='cart'),
    path('cart/add/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]