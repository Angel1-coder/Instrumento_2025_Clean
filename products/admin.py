from django.contrib import admin
from .models import Category, Product, SubscriptionPlan, RentalSubscription, RentalItem, LessonBooking


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    list_editable = ('friendly_name',)
    search_fields = ('name', 'friendly_name')
    ordering = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available_for_rental', 'available_for_purchase', 'stock_quantity', 'condition')
    list_filter = ('category', 'available_for_rental', 'available_for_purchase', 'condition')
    search_fields = ('name', 'description', 'sku')
    list_editable = ('price', 'available_for_rental', 'available_for_purchase', 'stock_quantity', 'condition')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'sku', 'description', 'image', 'image_url')
        }),
        ('Pricing', {
            'fields': ('price', 'rental_price_3_months', 'rental_price_6_months', 'rental_price_12_months', 'rental_price_24_months')
        }),
        ('Availability', {
            'fields': ('available_for_rental', 'available_for_purchase', 'stock_quantity')
        }),
        ('Condition & Status', {
            'fields': ('condition', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_months', 'monthly_price', 'setup_fee', 'insurance_included', 'lessons_included', 'max_instruments', 'is_active')
    list_filter = ('duration_months', 'insurance_included', 'lessons_included', 'is_active')
    list_editable = ('monthly_price', 'setup_fee', 'insurance_included', 'lessons_included', 'max_instruments', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('duration_months',)


class RentalItemInline(admin.TabularInline):
    model = RentalItem
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('product', 'rental_start', 'rental_end', 'monthly_rental_price', 'insurance_coverage', 'returned')


class LessonBookingInline(admin.TabularInline):
    model = LessonBooking
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('instructor_name', 'lesson_date', 'duration_minutes', 'lesson_type', 'status')


class RentalSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'status', 'total_cost', 'monthly_payment', 'insurance_opted')
    list_filter = ('status', 'plan', 'insurance_opted', 'start_date')
    search_fields = ('user__username', 'user__email', 'plan__name')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    
    inlines = [RentalItemInline, LessonBookingInline]
    
    fieldsets = (
        ('Subscription Details', {
            'fields': ('user', 'plan', 'start_date', 'end_date', 'status')
        }),
        ('Financial Information', {
            'fields': ('total_cost', 'monthly_payment', 'setup_fee_paid', 'insurance_opted', 'insurance_cost')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


class RentalItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'subscription', 'rental_start', 'rental_end', 'monthly_rental_price', 'insurance_coverage', 'returned')
    list_filter = ('insurance_coverage', 'returned', 'rental_start', 'rental_end')
    search_fields = ('product__name', 'subscription__user__username')
    list_editable = ('monthly_rental_price', 'insurance_coverage', 'returned')
    readonly_fields = ('created_at',)


class LessonBookingAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'instructor_name', 'lesson_date', 'duration_minutes', 'lesson_type', 'status')
    list_filter = ('status', 'lesson_type', 'lesson_date')
    search_fields = ('subscription__user__username', 'instructor_name')
    list_editable = ('status', 'lesson_date', 'duration_minutes')
    readonly_fields = ('created_at',)


# Register models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(RentalSubscription, RentalSubscriptionAdmin)
admin.site.register(RentalItem, RentalItemAdmin)
admin.site.register(LessonBooking, LessonBookingAdmin)



