#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product

# Korrekte Rental-Preise basierend auf dem ursprünglichen Repository
products_data = [
    {'id': 1, 'name': 'Yamaha FG800', 'purchase_price': 1799.95, 'rental_price_3months': 89.99, 'rental_price_6months': 79.99, 'rental_price_12months': 69.99, 'rental_price_24months': 59.99, 'student_discount_percentage': 10},
    {'id': 2, 'name': 'Fender CD-60S', 'purchase_price': 1299.99, 'rental_price_3months': 64.99, 'rental_price_6months': 57.99, 'rental_price_12months': 49.99, 'rental_price_24months': 44.99, 'student_discount_percentage': 10},
    {'id': 3, 'name': 'Squier Stratocaster', 'purchase_price': 2499.99, 'rental_price_3months': 124.99, 'rental_price_6months': 109.99, 'rental_price_12months': 99.99, 'rental_price_24months': 89.99, 'student_discount_percentage': 10},
    {'id': 4, 'name': 'Epiphone Les Paul', 'purchase_price': 1899.99, 'rental_price_3months': 94.99, 'rental_price_6months': 84.99, 'rental_price_12months': 74.99, 'rental_price_24months': 69.99, 'student_discount_percentage': 10},
    {'id': 5, 'name': 'Squier Precision Bass', 'purchase_price': 899.99, 'rental_price_3months': 44.99, 'rental_price_6months': 39.99, 'rental_price_12months': 34.99, 'rental_price_24months': 29.99, 'student_discount_percentage': 10},
    {'id': 6, 'name': 'Pearl Export Drum Kit', 'purchase_price': 3499.99, 'rental_price_3months': 174.99, 'rental_price_6months': 154.99, 'rental_price_12months': 139.99, 'rental_price_24months': 124.99, 'student_discount_percentage': 10},
    {'id': 7, 'name': 'Meinl Cajón', 'purchase_price': 299.99, 'rental_price_3months': 14.99, 'rental_price_6months': 12.99, 'rental_price_12months': 11.99, 'rental_price_24months': 9.99, 'student_discount_percentage': 10},
    {'id': 8, 'name': 'Yamaha YTR-2330 Trumpet', 'purchase_price': 3999.99, 'rental_price_3months': 199.99, 'rental_price_6months': 179.99, 'rental_price_12months': 159.99, 'rental_price_24months': 144.99, 'student_discount_percentage': 10},
    {'id': 9, 'name': 'Yamaha YAS-280 Saxophone', 'purchase_price': 5999.99, 'rental_price_3months': 299.99, 'rental_price_6months': 269.99, 'rental_price_12months': 239.99, 'rental_price_24months': 219.99, 'student_discount_percentage': 10},
    {'id': 10, 'name': 'Yamaha YFL-222 Flute', 'purchase_price': 199.99, 'rental_price_3months': 9.99, 'rental_price_6months': 8.99, 'rental_price_12months': 7.99, 'rental_price_24months': 6.99, 'student_discount_percentage': 10},
    {'id': 11, 'name': 'Yamaha P-45 Digital Piano', 'purchase_price': 5999.99, 'rental_price_3months': 299.99, 'rental_price_6months': 269.99, 'rental_price_12months': 239.99, 'rental_price_24months': 219.99, 'student_discount_percentage': 10},
    {'id': 12, 'name': 'Alesis V49 MIDI Keyboard', 'purchase_price': 299.99, 'rental_price_3months': 14.99, 'rental_price_6months': 12.99, 'rental_price_12months': 11.99, 'rental_price_24months': 9.99, 'student_discount_percentage': 10},
]

print("Setze alle korrekten Preise und Rental-Preise...")

for product_data in products_data:
    try:
        product = Product.objects.get(id=product_data['id'])
        
        # Setze purchase_price (das ist das, was im Template angezeigt wird)
        if hasattr(product, 'purchase_price'):
            product.purchase_price = product_data['purchase_price']
        
        # Setze rental prices (ohne Unterstrich, wie im ursprünglichen Repository)
        if hasattr(product, 'rental_price_3months'):
            product.rental_price_3months = product_data['rental_price_3months']
        if hasattr(product, 'rental_price_6months'):
            product.rental_price_6months = product_data['rental_price_6months']
        if hasattr(product, 'rental_price_12months'):
            product.rental_price_12months = product_data['rental_price_12months']
        if hasattr(product, 'rental_price_24months'):
            product.rental_price_24months = product_data['rental_price_24months']
        
        # Setze student discount
        if hasattr(product, 'student_discount_percentage'):
            product.student_discount_percentage = product_data['student_discount_percentage']
        
        product.save()
        print(f"✅ {product.name}: Purchase: €{product_data['purchase_price']}, Rental 6m: €{product_data['rental_price_6months']}/month")
        
    except Product.DoesNotExist:
        print(f"❌ Produkt ID {product_data['id']} nicht gefunden")

print("\nAlle Preise wurden korrigiert!")

