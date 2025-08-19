from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, SubscriptionPlan, RentalItem, RentalSubscription, InsuranceOption
from .forms import ProductForm

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def subscription_plans(request):
    """View to show all available subscription plans"""
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('duration_months')
    
    context = {
        'plans': plans,
    }
    return render(request, 'products/subscription_plans.html', context)


@login_required
def rental_checkout(request, product_id, plan_id):
    """View for rental checkout with subscription plan"""
    product = get_object_or_404(Product, pk=product_id)
    plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    insurance_options = InsuranceOption.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Handle rental subscription creation
        insurance_type = request.POST.get('insurance_type', 'none')
        insurance_option = None
        
        if insurance_type != 'none':
            insurance_option = get_object_or_404(InsuranceOption, name=insurance_type)
        
        # Create rental subscription
        from django.utils import timezone
        from datetime import timedelta
        
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=plan.duration_months * 30)
        
        subscription = RentalSubscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            total_cost=plan.get_total_cost(),
            monthly_payment=plan.monthly_price,
            insurance_opted=insurance_type != 'none',
            insurance_cost=insurance_option.monthly_cost * plan.duration_months if insurance_option else 0,
        )
        
        # Create rental item
        rental_item = RentalItem.objects.create(
            subscription=subscription,
            product=product,
            rental_start=start_date,
            rental_end=end_date,
            monthly_rental_price=plan.monthly_price,
            insurance_coverage=insurance_type != 'none',
            insurance_cost=insurance_option.monthly_cost if insurance_option else 0,
            condition_at_start=product.condition,
        )
        
        messages.success(request, f'Rental subscription created successfully! Subscription #{subscription.id}')
        return redirect('rental_success', subscription.id)
    
    context = {
        'product': product,
        'plan': plan,
        'insurance_options': insurance_options,
    }
    return render(request, 'products/rental_checkout.html', context)


@login_required
def rental_success(request, subscription_id):
    """View for successful rental subscriptions"""
    subscription = get_object_or_404(RentalSubscription, pk=subscription_id, user=request.user)
    
    context = {
        'subscription': subscription,
    }
    return render(request, 'products/rental_success.html', context)


@login_required
def my_rentals(request):
    """View for users to see their rental history"""
    subscriptions = RentalSubscription.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'subscriptions': subscriptions,
    }
    return render(request, 'products/my_rentals.html', context)


def rental_instruments(request):
    """Display all instruments available for rental"""
    products = Product.objects.filter(available_for_rental=True).order_by('name')
    
    context = {
        'products': products,
    }
    
    return render(request, 'products/rental_instruments.html', context)


def special_offers(request):
    """Display special offers page"""
    return render(request, 'products/special_offers.html')


def test_buttons(request):
    """Test page for debugging button functionality"""
    return render(request, 'products/test_buttons.html')


def add_temp_to_bag(request):
    """Add a temporary product to bag for testing"""
    # Get plan and price from URL parameters
    plan_months = request.GET.get('plan', '6')
    rental_price = request.GET.get('price', '0')
    rental_type = request.GET.get('type', 'purchase')
    product_id = request.GET.get('product_id', '')
    
    # Clear the old bag completely
    request.session['bag'] = {}
    
    if rental_type == 'rental':
        # This is a rental subscription
        try:
            # Get the specific product if product_id is provided, otherwise get first available
            if product_id:
                product = get_object_or_404(Product, pk=product_id, available_for_rental=True)
            else:
                product = Product.objects.filter(available_for_rental=True).first()
                
            if product:
                # Fix German number format (comma to dot) and convert to float
                rental_price_clean = rental_price.replace(',', '.')
                monthly_price = float(rental_price_clean)
                
                # Create a rental subscription entry
                rental_data = {
                    'product_id': str(product.id),
                    'product_name': product.name,
                    'plan_months': int(plan_months),
                    'monthly_price': monthly_price,
                    'type': 'rental_subscription'
                }
                
                # Add to bag with rental information
                bag = {'rental_subscription': rental_data}
                request.session['bag'] = bag
                
                messages.success(
                    request, 
                    f'Rental subscription for {product.name} ({plan_months} months) added to bag!'
                )
            else:
                # No rental products available
                messages.error(request, 'No rental products available')
                return redirect('rental_instruments')
                
        except Exception as e:
            messages.error(request, f'Error adding rental subscription: {e}')
            return redirect('rental_instruments')
    else:
        # This is a regular purchase (fallback)
        try:
            first_product = Product.objects.first()
            if first_product:
                bag = {str(first_product.id): 1}
                request.session['bag'] = bag
                messages.success(request, f'Product "{first_product.name}" added to bag!')
            else:
                bag = {'dummy_1': 1}
                request.session['bag'] = bag
                messages.success(request, 'Test product added to bag!')
        except Exception as e:
            bag = {'dummy_1': 1}
            request.session['bag'] = bag
            messages.success(request, 'Test product added to bag!')
    
    return redirect('checkout')

