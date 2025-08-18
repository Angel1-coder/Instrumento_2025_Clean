from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid


class Category(models.Model):
    """
    Category model for organizing instruments
    """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    Product model for musical instruments
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rental_price_3_months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rental_price_6_months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rental_price_12_months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rental_price_24_months = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    available_for_rental = models.BooleanField(default=True)
    available_for_purchase = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=50, choices=[
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], default='very_good')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_rental_price(self, months):
        """Get rental price for specific duration"""
        if months == 3 and self.rental_price_3_months:
            return self.rental_price_3_months
        elif months == 6 and self.rental_price_6_months:
            return self.rental_price_6_months
        elif months == 12 and self.rental_price_12_months:
            return self.rental_price_12_months
        elif months == 24 and self.rental_price_24_months:
            return self.rental_price_24_months
        return None


class SubscriptionPlan(models.Model):
    """
    Subscription plan model for instrument rentals
    """
    name = models.CharField(max_length=100)
    duration_months = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(24)]
    )
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    setup_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    insurance_included = models.BooleanField(default=False)
    lessons_included = models.BooleanField(default=True)
    max_instruments = models.PositiveIntegerField(default=1)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['duration_months']

    def __str__(self):
        return f"{self.name} ({self.duration_months} months)"

    def get_total_cost(self):
        """Calculate total cost for the subscription period"""
        return (self.monthly_price * self.duration_months) + self.setup_fee


class InsuranceOption(models.Model):
    """
    Insurance options for instrument rentals
    """
    name = models.CharField(max_length=254)
    description = models.TextField()
    monthly_cost = models.DecimalField(max_digits=8, decimal_places=2)
    coverage_amount = models.DecimalField(max_digits=8, decimal_places=2)
    deductible = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RentalSubscription(models.Model):
    """
    Active rental subscription for users
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=6, decimal_places=2)
    setup_fee_paid = models.BooleanField(default=False)
    insurance_opted = models.BooleanField(default=False)
    insurance_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def is_active(self):
        """Check if subscription is currently active"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date

    def get_remaining_days(self):
        """Get remaining days in subscription"""
        from django.utils import timezone
        today = timezone.now().date()
        if self.end_date > today:
            return (self.end_date - today).days
        return 0


class RentalItem(models.Model):
    """
    Individual instrument rental within a subscription
    """
    subscription = models.ForeignKey(RentalSubscription, on_delete=models.CASCADE, related_name='rental_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    rental_start = models.DateField()
    rental_end = models.DateField()
    monthly_rental_price = models.DecimalField(max_digits=6, decimal_places=2)
    insurance_coverage = models.BooleanField(default=False)
    insurance_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    condition_at_start = models.CharField(max_length=50, choices=Product._meta.get_field('condition').choices)
    condition_at_return = models.CharField(max_length=50, choices=Product._meta.get_field('condition').choices, null=True, blank=True)
    notes = models.TextField(blank=True)
    returned = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.subscription.user.username}"

    def is_currently_rented(self):
        """Check if item is currently being rented"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.rental_start <= today <= self.rental_end and not self.returned

    def get_rental_duration_days(self):
        """Get total rental duration in days"""
        return (self.rental_end - self.rental_start).days


class LessonBooking(models.Model):
    """
    Music lesson bookings for subscription holders
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    subscription = models.ForeignKey(RentalSubscription, on_delete=models.CASCADE, related_name='lesson_bookings')
    instructor_name = models.CharField(max_length=100)
    lesson_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    lesson_type = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('technique', 'Technique Focus'),
        ('repertoire', 'Repertoire Building'),
    ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['lesson_date']

    def __str__(self):
        return f"{self.subscription.user.username} - {self.lesson_type} on {self.lesson_date.strftime('%Y-%m-%d')}"

    def is_upcoming(self):
        """Check if lesson is in the future"""
        from django.utils import timezone
        return self.lesson_date > timezone.now() and self.status == 'scheduled'
