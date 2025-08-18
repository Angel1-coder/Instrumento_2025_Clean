#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product

# Setze Rental-Preise für alle Produkte
products = Product.objects.all()

for product in products:
    # Setze Rental-Preise basierend auf dem Kaufpreis (etwa 5-10% pro Monat)
    if product.price:
        base_monthly = float(product.price) * 0.05  # 5% des Kaufpreises pro Monat
        
        product.rental_price_3_months = round(base_monthly * 1.2, 2)  # 20% mehr für kurze Miete
        product.rental_price_6_months = round(base_monthly, 2)  # Standard-Preis
        product.rental_price_12_months = round(base_monthly * 0.8, 2)  # 20% Rabatt für lange Miete
        product.rental_price_24_months = round(base_monthly * 0.6, 2)  # 40% Rabatt für sehr lange Miete
        
        product.save()
        print(f"✅ {product.name}: 3m:€{product.rental_price_3_months}, 6m:€{product.rental_price_6_months}, 12m:€{product.rental_price_12_months}, 24m:€{product.rental_price_24_months}")

print("\nAlle Rental-Preise wurden gesetzt!")

