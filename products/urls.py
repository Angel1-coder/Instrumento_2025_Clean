from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/',
         views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/',
         views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product, name='delete_product'),
    # Subscription and rental URLs
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('rental-checkout/<int:product_id>/<int:plan_id>/', 
         views.rental_checkout, name='rental_checkout'),
    path('rental-success/<str:order_number>/', 
         views.rental_success, name='rental_success'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('rental-instruments/', views.rental_instruments, name='rental_instruments'),
]
