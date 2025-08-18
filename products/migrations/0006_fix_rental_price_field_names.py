# Generated manually to fix rental price field names

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_add_price_field_back'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='rental_price_3months',
            new_name='rental_price_3_months',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='rental_price_6months',
            new_name='rental_price_6_months',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='rental_price_12months',
            new_name='rental_price_12_months',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='rental_price_24months',
            new_name='rental_price_24_months',
        ),
    ]



