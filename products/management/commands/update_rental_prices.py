from django.core.management.base import BaseCommand
from products.models import Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update rental prices for all instruments with profitable pricing structure'

    def handle(self, *args, **options):
        self.stdout.write('Updating rental prices for all instruments...')
        
        # Get all products
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            # Calculate rental prices based on purchase price
            # 3 months: 18% of purchase price per month (higher for short term)
            # 6 months: 12% of purchase price per month (best value - OPTIMIZED!)
            # 12 months: 9% of purchase price per month (longer commitment)
            # 24 months: 6% of purchase price per month (longest commitment)
            
            purchase_price = product.price
            
            # 3 months - higher monthly cost, less discount
            rental_3_months = round(purchase_price * Decimal('0.18'), 2)
            
            # 6 months - OPTIMIZED pricing, better discount for medium commitment
            rental_6_months = round(purchase_price * Decimal('0.12'), 2)
            
            # 12 months - good discount for longer commitment
            rental_12_months = round(purchase_price * Decimal('0.09'), 2)
            
            # 24 months - maximum discount for longest commitment
            rental_24_months = round(purchase_price * Decimal('0.06'), 2)
            
            # Update the product
            product.rental_price_3_months = rental_3_months
            product.rental_price_6_months = rental_6_months
            product.rental_price_12_months = rental_12_months
            product.rental_price_24_months = rental_24_months
            
            product.save()
            updated_count += 1
            
            self.stdout.write(
                f'Updated {product.name}: '
                f'3m: €{rental_3_months}, '
                f'6m: €{rental_6_months}, '
                f'12m: €{rental_12_months}, '
                f'24m: €{rental_24_months}'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated rental prices for {updated_count} products!'
            )
        )
        
        # Display summary of pricing strategy
        self.stdout.write('\n' + '='*60)
        self.stdout.write('OPTIMIZED RENTAL PRICING STRATEGY:')
        self.stdout.write('='*60)
        self.stdout.write('3 Months:  18% of purchase price/month (Try & Test)')
        self.stdout.write('6 Months:  12% of purchase price/month (Best Value - OPTIMIZED!)')
        self.stdout.write('12 Months:  9% of purchase price/month (Serious Musician)')
        self.stdout.write('24 Months:  6% of purchase price/month (Long-term)')
        self.stdout.write('='*60)
        self.stdout.write('6-Months now offers 33% discount vs 3-months!')
        self.stdout.write('This pricing ensures profitability for both customer and seller:')
        self.stdout.write('• Customer gets significant savings on longer commitments')
        self.stdout.write('• Seller recovers investment within 6-8 months')
        self.stdout.write('• Flexible options for different commitment levels')
        self.stdout.write('• 6-months is now truly attractive!')
