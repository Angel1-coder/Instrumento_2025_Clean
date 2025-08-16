from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    """
    Send confirmation email when order is created
    """
    if created:
        # Send confirmation email to customer
        subject = f'Order Confirmation - {instance.order_number}'
        
        # Prepare email context
        context = {
            'order': instance,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
        }
        
        # Render email templates
        email_body = render_to_string('checkout/confirmation_emails/confirmation_email_body.txt', context)
        email_subject = render_to_string('checkout/confirmation_emails/confirmation_email_subject.txt', context)
        
        # Send email
        send_mail(
            subject=email_subject.strip(),
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
        
        # Also send notification to admin
        admin_subject = f'New Order Received - {instance.order_number}'
        admin_body = f'New order received from {instance.full_name} for {instance.grand_total}'
        
        send_mail(
            subject=admin_subject,
            message=admin_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else [settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )


@receiver(post_save, sender=Order)
def save_order(sender, instance, **kwargs):
    """
    Update user profile when order is saved
    """
    # Update user profile if user is authenticated
    if instance.user_profile:
        profile = instance.user_profile
        profile.default_phone_number = instance.phone_number
        profile.default_country = instance.country
        profile.default_postcode = instance.postcode
        profile.default_town_or_city = instance.town_or_city
        profile.default_street_address1 = instance.street_address1
        profile.default_street_address2 = instance.street_address2
        profile.default_county = instance.county
        profile.save()


@receiver(post_delete, sender=Order)
def delete_order(sender, instance, **kwargs):
    """
    Handle order deletion if needed
    """
    pass


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()
