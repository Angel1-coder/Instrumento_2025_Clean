#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product

print("Aktualisiere ein bestehendes Produkt zu einem realistischen Fender-Beispiel...")

# Take the first available product and make it a Fender
try:
    # Finde ein Produkt (z.B. das erste)
    product = Product.objects.first()
    
    if product:
        # Aktualisiere es zu einem realistischen Fender
        product.name = 'Fender American Professional II Stratocaster'
        product.description = 'Die legendäre Fender Stratocaster in ihrer besten Ausführung. Handgefertigt in Corona, Kalifornien mit Premium-Komponenten und dem berühmten Strat-Sound. Perfekt für Studio, Bühne und Übungsraum.'
        product.price = 1899.99
        product.rental_price_3_months = 219.99  # 11.6% des Kaufpreises
        product.rental_price_6_months = 199.99  # 10.5% des Kaufpreises
        product.rental_price_12_months = 179.99 # 9.5% des Kaufpreises
        product.rental_price_24_months = 159.99 # 8.4% des Kaufpreises
        product.sku = 'FENDER-STRAT-PRO-II'
        product.condition = 'excellent'
        product.available_for_rental = True
        product.available_for_purchase = True
        product.stock_quantity = 3
        product.image_url = 'https://images.pexels.com/photos/1327430/pexels-photo-1327430.jpeg?w=800&h=600&fit=crop'
        
        product.save()
        
        print(f"✅ Produkt erfolgreich aktualisiert!")
        print(f"🎸 {product.name}")
        print(f"   ID: {product.id}")
        print(f"   Kaufpreis: €{product.price}")
        print(f"   3 Monate: €{product.rental_price_3_months}/Monat (11.6%)")
        print(f"   6 Monate: €{product.rental_price_6_months}/Monat (10.5%)")
        print(f"   12 Monate: €{product.rental_price_12_months}/Monat (9.5%)")
        print(f"   24 Monate: €{product.rental_price_24_months}/Monat (8.4%)")
        print(f"   SKU: {product.sku}")
        print(f"   Zustand: {product.condition}")
        print(f"   Verfügbar für Miete: {'Ja' if product.available_for_rental else 'Nein'}")
        print(f"   Vorrat: {product.stock_quantity}")
        
        print(f"\n💡 Jetzt haben wir ein realistisches Beispiel!")
        print(f"   - Wirtschaftlich sinnvolle Mietpreise")
        print(f"   - Echte Fender-Gitarre")
        print(f"   - Professionelle Beschreibung")
        
    else:
        print("❌ Keine Produkte in der Datenbank gefunden")
        
except Exception as e:
    print(f"❌ Fehler: {e}")

print("\nDas Fender-Beispiel wurde erfolgreich erstellt! 🎸")
print("Besuchen Sie http://127.0.0.1:8000/products/ um es zu sehen.")




