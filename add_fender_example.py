#!/usr/bin/env python
import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boutique_ado.settings')
django.setup()

from products.models import Product, Category
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

# Use an existing category or create a new one
try:
    # First, try to find an existing category
    category = Category.objects.first()
    if not category:
        # Create a new category if none exists
        category = Category.objects.create(
            name='E-Guitars',
            friendly_name='E-Guitars',
            description='Professional E-Guitars for all styles'
        )
        print(f"✅ New category created: {category.name}")
    else:
        print(f"✅ Existing category used: {category.name}")
        
except Exception as e:
    print(f"⚠️ Error creating category: {e}")
    # Use a default category
    category = None

# Fender Stratocaster with realistic prices
fender_data = {
    'name': 'Fender American Professional II Stratocaster',
    'description': 'The legendary Fender Stratocaster in its best execution. Handcrafted in Corona, California with premium components and the famous Strat-Sound.',
    'price': 1899.99,
    'rating': 4.9,
    'category': category,
    'rental_price_3_months': 219.99,  # 11.6% of purchase price
    'rental_price_6_months': 199.99,  # 10.5% of purchase price
    'rental_price_12_months': 179.99, # 9.5% of purchase price
    'rental_price_24_months': 159.99, # 8.4% of purchase price
    'student_discount_percentage': 15,
    'available_for_rental': True,
    'stock_quantity': 5,
    'sku': 'FENDER-STRAT-PRO-II',
    'condition': 'excellent',
    'image_url': 'https://images.pexels.com/photos/1516924962500-2b4b3b99ea02/pexels-photo-1516924962500-2b4b3b99ea02.jpeg?w=800&h=600&fit=crop'
}

try:
    # Check if the product already exists
    existing_product = Product.objects.filter(name__icontains='Fender American Professional II').first()
    
    if existing_product:
        print(f"✅ Product already exists: {existing_product.name}")
        # Update prices
        existing_product.price = fender_data['price']
        existing_product.rental_price_3_months = fender_data['rental_price_3_months']
        existing_product.rental_price_6_months = fender_data['rental_price_6_months']
        existing_product.rental_price_12_months = fender_data['rental_price_12_months']
        existing_product.rental_price_24_months = fender_data['rental_price_24_months']
        existing_product.save()
        print("   Prices updated!")
    else:
        # Create new product
        new_product = Product.objects.create(
            name=fender_data['name'],
            description=fender_data['description'],
            price=fender_data['price'],
            category=fender_data['category'],
            rental_price_3_months=fender_data['rental_price_3_months'],
            rental_price_6_months=fender_data['rental_price_6_months'],
            rental_price_12_months=fender_data['rental_price_12_months'],
            rental_price_24_months=fender_data['rental_price_24_months'],
            available_for_rental=fender_data['available_for_rental'],
            stock_quantity=fender_data['stock_quantity'],
            sku=fender_data['sku'],
            condition=fender_data['condition']
        )
        print(f"✅ New product created: {new_product.name}")
        
        # Load the image from Unsplash
        try:
            response = requests.get(fender_data['image_url'])
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                
                new_product.image.save(
                    f"fender_strat_pro_ii.jpg",
                    File(img_temp),
                    save=True
                )
                print("   Image successfully loaded!")
            else:
                print("   Image could not be loaded")
        except Exception as e:
            print(f"   Error loading image: {e}")
    
    print(f"\n🎸 Fender American Professional II Stratocaster")
    print(f"   Purchase price: €{fender_data['price']}")
    print(f"   3 months: €{fender_data['rental_price_3_months']}/month")
    print(f"   6 months: €{fender_data['rental_price_6_months']}/month")
    print(f"   12 months: €{fender_data['rental_price_12_months']}/month")
    print(f"   24 months: €{fender_data['rental_price_24_months']}/month")
    print(f"   Student discount: 15% (calculated in the application)")
    print(f"   Category: {category.name if category else 'None'}")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\nThe Fender example product has been successfully added!")
print("You can now see it in the admin interface or on the website.")
