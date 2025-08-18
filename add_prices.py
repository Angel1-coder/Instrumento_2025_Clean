#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product

# Preise für alle Produkte hinzufügen
products_data = [
    {'id': 1, 'name': 'Saxophone', 'price': 299.99, 'rating': 4.8},
    {'id': 2, 'name': 'Trumpet', 'price': 199.99, 'rating': 4.6},
    {'id': 3, 'name': 'Violin', 'price': 149.99, 'rating': 4.7},
    {'id': 4, 'name': 'Bass Guitar', 'price': 399.99, 'rating': 4.9},
    {'id': 5, 'name': 'Electric Guitar', 'price': 349.99, 'rating': 4.8},
    {'id': 6, 'name': 'Cajón', 'price': 89.99, 'rating': 4.5},
    {'id': 7, 'name': 'Hang', 'price': 599.99, 'rating': 4.9},
    {'id': 8, 'name': 'Piano', 'price': 1299.99, 'rating': 4.9},
    {'id': 9, 'name': 'Frequency Bowl (Yoga)', 'price': 79.99, 'rating': 4.4},
]

print("Füge Preise zu Produkten hinzu...")

for product_data in products_data:
    try:
        product = Product.objects.get(id=product_data['id'])
        product.price = product_data['price']
        product.rating = product_data['rating']
        product.save()
        print(f"✅ {product.name}: €{product.price} (Rating: {product.rating})")
    except Product.DoesNotExist:
        print(f"❌ Produkt {product_data['name']} nicht gefunden")

print("\nAlle Preise wurden hinzugefügt!")


