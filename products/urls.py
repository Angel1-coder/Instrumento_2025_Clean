from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('rental-checkout/<int:product_id>/', views.rental_checkout, name='rental_checkout'),
    path('rental-success/<int:subscription_id>/', views.rental_success, name='rental_success'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('rental-instruments/', views.rental_instruments, name='rental_instruments'),
    path('special-offers/', views.special_offers, name='special_offers'),
    path('test-buttons/', views.test_buttons, name='test_buttons'),
    path('add-temp-to-bag/', views.add_temp_to_bag, name='add_temp_to_bag'),
]
