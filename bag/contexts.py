from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # Check if this is a rental subscription
    if 'rental_subscription' in bag:
        rental_data = bag['rental_subscription']
        
        # Create a rental subscription item
        rental_item = {
            'item_id': 'rental_subscription',
            'quantity': 1,
            'product': type('RentalProduct', (), {
                'id': rental_data['product_id'],
                'name': f"{rental_data['product_name']} - {rental_data['plan_months']} Month Rental",
                'price': Decimal(str(rental_data['monthly_price'])),
                'image': None,
                'is_rental': True,
                'plan_months': rental_data['plan_months']
            })(),
            'is_rental': True,
            'plan_months': rental_data['plan_months'],
            'monthly_price': Decimal(str(rental_data['monthly_price']))
        }
        
        bag_items.append(rental_item)
        # Only show monthly price, not total for entire period
        total = rental_data['monthly_price']  # Just monthly price
        product_count = 1
        
        # Calculate delivery (free for rentals)
        delivery = 0
        free_delivery_delta = 0
        
        grand_total = total + delivery
        
        context = {
            'bag_items': bag_items,
            'total': total,
            'product_count': product_count,
            'delivery': delivery,
            'free_delivery_delta': free_delivery_delta,
            'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
            'grand_total': grand_total,
            'is_rental': True,
        }
        
        return context

    # Regular product processing (existing code)
    for item_id, item_data in bag.items():

        # Handle dummy products for testing
        if item_id.startswith('dummy_'):
            # Create a dummy product for testing
            dummy_product = type('DummyProduct', (), {
                'id': item_id,
                'name': 'Test Product',
                'price': Decimal('99.99'),
                'image': None
            })()
            
            total += item_data * dummy_product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': dummy_product,
            })
            continue

        try:
            if isinstance(item_data, int):
                product = get_object_or_404(Product, pk=item_id)
                total += item_data * product.price
                product_count += item_data
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                })

            else:
                product = get_object_or_404(Product, pk=item_id)
                for size, quantity in item_data['items_by_size'].items():
                    total += quantity * product.price
                    product_count += quantity
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                        'size': size,
                    })
        except Exception as e:
            # Skip invalid products and log the error
            print(f"Error processing product {item_id}: {e}")
            continue

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'is_rental': False,
    }

    return context
