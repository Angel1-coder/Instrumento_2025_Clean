#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product

# Korrekte Preise aus dem ursprünglichen Instrumento Repository
products_data = [
    {'id': 1, 'name': 'Yamaha FG800', 'price': 1799.95, 'rating': 4.8},
    {'id': 2, 'name': 'Fender CD-60S', 'price': 1299.99, 'rating': 4.7},
    {'id': 3, 'name': 'Squier Stratocaster', 'price': 2499.99, 'rating': 4.9},
    {'id': 4, 'name': 'Epiphone Les Paul', 'price': 1899.99, 'rating': 4.8},
    {'id': 5, 'name': 'Squier Precision Bass', 'price': 899.99, 'rating': 4.6},
    {'id': 6, 'name': 'Pearl Export Drum Kit', 'price': 3499.99, 'rating': 4.9},
    {'id': 7, 'name': 'Meinl Cajón', 'price': 299.99, 'rating': 4.7},
    {'id': 8, 'name': 'Yamaha YTR-2330 Trumpet', 'price': 3999.99, 'rating': 4.9},
    {'id': 9, 'name': 'Yamaha YAS-280 Saxophone', 'price': 5999.99, 'rating': 4.9},
    {'id': 10, 'name': 'Yamaha YFL-222 Flute', 'price': 199.99, 'rating': 4.5},
    {'id': 11, 'name': 'Yamaha P-45 Digital Piano', 'price': 5999.99, 'rating': 4.9},
    {'id': 12, 'name': 'Alesis V49 MIDI Keyboard', 'price': 299.99, 'rating': 4.6},
]

print("Setze alle korrekten Preise aus dem ursprünglichen Repository...")

for product_data in products_data:
    try:
        product = Product.objects.get(id=product_data['id'])
        product.price = product_data['price']
        product.rating = product_data['rating']
        product.save()
        print(f"✅ {product.name}: €{product.price} (Rating: {product.rating})")
    except Product.DoesNotExist:
        print(f"❌ Produkt ID {product_data['id']} nicht gefunden")

print("\nAlle Preise wurden korrigiert!")


