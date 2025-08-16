from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, SubscriptionPlan, RentalOrder, InsuranceOption
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
        # Handle rental order creation
        insurance_type = request.POST.get('insurance_type', 'none')
        insurance_option = None
        
        if insurance_type != 'none':
            insurance_option = get_object_or_404(InsuranceOption, name=insurance_type)
        
        # Create rental order
        rental_order = RentalOrder.objects.create(
            user=request.user,
            product=product,
            rental_duration=plan.duration_months,
            monthly_price=plan.monthly_price,
            total_price=plan.total_price,
            insurance_type=insurance_type,
            insurance_cost=insurance_option.monthly_cost * plan.duration_months if insurance_option else 0,
        )
        
        messages.success(request, f'Rental order created successfully! Order #{rental_order.order_number}')
        return redirect('rental_success', rental_order.order_number)
    
    context = {
        'product': product,
        'plan': plan,
        'insurance_options': insurance_options,
    }
    return render(request, 'products/rental_checkout.html', context)


@login_required
def rental_success(request, order_number):
    """View for successful rental orders"""
    rental_order = get_object_or_404(RentalOrder, order_number=order_number, user=request.user)
    
    context = {
        'rental_order': rental_order,
    }
    return render(request, 'products/rental_success.html', context)


@login_required
def my_rentals(request):
    """View for users to see their rental history"""
    rental_orders = RentalOrder.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'rental_orders': rental_orders,
    }
    return render(request, 'products/my_rentals.html', context)
