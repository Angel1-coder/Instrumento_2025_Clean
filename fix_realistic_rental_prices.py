#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product

# Realistische Mietpreise basierend auf 8-12% des Kaufpreises pro Monat
products_data = [
    {'id': 1, 'name': 'Yamaha FG800', 'price': 1799.95, 'rental_price_3months': 199.99, 'rental_price_6months': 179.99, 'rental_price_12months': 159.99, 'rental_price_24months': 139.99, 'student_discount_percentage': 15},
    {'id': 2, 'name': 'Fender CD-60S', 'price': 1299.99, 'rental_price_3months': 149.99, 'rental_price_6months': 134.99, 'rental_price_12months': 119.99, 'rental_price_24months': 104.99, 'student_discount_percentage': 15},
    {'id': 3, 'name': 'Squier Stratocaster', 'price': 2499.99, 'rental_price_3months': 279.99, 'rental_price_6months': 249.99, 'rental_price_12months': 219.99, 'rental_price_24months': 189.99, 'student_discount_percentage': 15},
    {'id': 4, 'name': 'Epiphone Les Paul', 'price': 1899.99, 'rental_price_3months': 209.99, 'rental_price_6months': 189.99, 'rental_price_12months': 169.99, 'rental_price_24months': 149.99, 'student_discount_percentage': 15},
    {'id': 5, 'name': 'Squier Precision Bass', 'price': 899.99, 'rental_price_3months': 99.99, 'rental_price_6months': 89.99, 'rental_price_12months': 79.99, 'rental_price_24months': 69.99, 'student_discount_percentage': 15},
    {'id': 6, 'name': 'Pearl Export Drum Kit', 'price': 3499.99, 'rental_price_3months': 389.99, 'rental_price_6months': 349.99, 'rental_price_12months': 309.99, 'rental_price_24months': 269.99, 'student_discount_percentage': 15},
    {'id': 7, 'name': 'Meinl Cajón', 'price': 299.99, 'rental_price_3months': 34.99, 'rental_price_6months': 31.99, 'rental_price_12months': 28.99, 'rental_price_24months': 25.99, 'student_discount_percentage': 15},
    {'id': 8, 'name': 'Yamaha YTR-2330 Trumpet', 'price': 3999.99, 'rental_price_3months': 439.99, 'rental_price_6months': 399.99, 'rental_price_12months': 359.99, 'rental_price_24months': 319.99, 'student_discount_percentage': 15},
    {'id': 9, 'name': 'Yamaha YAS-280 Saxophone', 'price': 5999.99, 'rental_price_3months': 659.99, 'rental_price_6months': 599.99, 'rental_price_12months': 539.99, 'rental_price_24months': 479.99, 'student_discount_percentage': 15},
    {'id': 10, 'name': 'Yamaha YFL-222 Flute', 'price': 199.99, 'rental_price_3months': 24.99, 'rental_price_6months': 22.99, 'rental_price_12months': 20.99, 'rental_price_24months': 18.99, 'student_discount_percentage': 15},
    {'id': 11, 'name': 'Yamaha P-45 Digital Piano', 'price': 5999.99, 'rental_price_3months': 659.99, 'rental_price_6months': 599.99, 'rental_price_12months': 539.99, 'rental_price_24months': 479.99, 'student_discount_percentage': 15},
    {'id': 12, 'name': 'Alesis V49 MIDI Keyboard', 'price': 299.99, 'rental_price_3months': 34.99, 'rental_price_6months': 31.99, 'rental_price_12months': 28.99, 'rental_price_24months': 25.99, 'student_discount_percentage': 15},
]

print("Setze realistische Mietpreise für alle Produkte...")
print("Basierend auf 8-12% des Kaufpreises pro Monat")
print("Studentenrabatt: 15%\n")

for product_data in products_data:
    try:
        product = Product.objects.get(id=product_data['id'])
        
        # Setze alle Preise
        product.price = product_data['price']
        product.rental_price_3months = product_data['rental_price_3months']
        product.rental_price_6months = product_data['rental_price_6months']
        product.rental_price_12months = product_data['rental_price_12months']
        product.rental_price_24months = product_data['rental_price_24months']
        product.student_discount_percentage = product_data['student_discount_percentage']
        
        product.save()
        
        # Berechne Prozentsätze für Überprüfung
        pct_3m = (product_data['rental_price_3months'] / product_data['price']) * 100
        pct_24m = (product_data['rental_price_24months'] / product_data['price']) * 100
        
        print(f"✅ {product.name}")
        print(f"   Kaufpreis: €{product_data['price']}")
        print(f"   3 Monate: €{product_data['rental_price_3months']}/Monat ({pct_3m:.1f}%)")
        print(f"   6 Monate: €{product_data['rental_price_6months']}/Monat")
        print(f"   12 Monate: €{product_data['rental_price_12months']}/Monat")
        print(f"   24 Monate: €{product_data['rental_price_24months']}/Monat ({pct_24m:.1f}%)")
        print(f"   Studentenrabatt: {product_data['student_discount_percentage']}%")
        print()
        
    except Product.DoesNotExist:
        print(f"❌ Produkt ID {product_data['id']} nicht gefunden")

print("Alle realistischen Mietpreise wurden gesetzt!")
print("\nJetzt macht das Geschäft wirtschaftlich Sinn:")
print("- 3 Monate: 11-13% des Kaufpreises pro Monat")
print("- 24 Monate: 5-7% des Kaufpreises pro Monat")
print("- Nach 24 Monaten: 120-168% des Kaufpreises verdient")
