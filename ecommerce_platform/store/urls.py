from django.urls import path
from . import views

app_name='store'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category', views.TeaListView.as_view(), name='shop'),
    path('category/<slug:slug>/', views.TeaListView.as_view(), name='category_page'),
    path('search/', views.TeaListView.as_view(), name='search'),
    path('product/<slug:slug>/', views.TeaDetailView.as_view(), name='product_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
]
