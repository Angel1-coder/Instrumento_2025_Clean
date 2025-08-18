#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product

# Korrekte Preise aus dem ursprünglichen Instrumento Projekt
products_data = [
    {'id': 1, 'name': 'Fender CD-60S', 'price': 1799.95, 'rating': 4.8},
    {'id': 2, 'name': 'Squier Telecaster', 'price': 1299.99, 'rating': 4.7},
    {'id': 3, 'name': 'Yamaha YAS-280 Saxophone', 'price': 2499.99, 'rating': 4.9},
    {'id': 4, 'name': 'Yamaha YTR-2330 Trumpet', 'price': 1899.99, 'rating': 4.8},
    {'id': 5, 'name': 'Violin Student Model', 'price': 899.99, 'rating': 4.6},
    {'id': 6, 'name': 'Bass Guitar Professional', 'price': 3499.99, 'rating': 4.9},
    {'id': 7, 'name': 'Meinl Cajón Professional', 'price': 299.99, 'rating': 4.7},
    {'id': 8, 'name': 'Hang Drum Premium', 'price': 3999.99, 'rating': 4.9},
    {'id': 9, 'name': 'Digital Piano Yamaha', 'price': 5999.99, 'rating': 4.9},
    {'id': 10, 'name': 'Frequency Bowl Set', 'price': 199.99, 'rating': 4.5},
]

print("Setze korrekte Preise für alle Produkte...")

for product_data in products_data:
    try:
        product = Product.objects.get(id=product_data['id'])
        product.price = product_data['price']
        product.rating = product_data['rating']
        product.save()
        print(f"✅ {product.name}: €{product.price} (Rating: {product.rating})")
    except Product.DoesNotExist:
        print(f"❌ Produkt ID {product_data['id']} nicht gefunden")

print("\nAlle korrekten Preise wurden gesetzt!")
