# Generated manually to add missing product fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_fix_rental_price_field_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_for_rental',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='available_for_purchase',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='product',
            name='condition',
            field=models.CharField(max_length=50, choices=[
                ('excellent', 'Excellent'),
                ('very_good', 'Very Good'),
                ('good', 'Good'),
                ('fair', 'Fair'),
                ('poor', 'Poor'),
            ], default='very_good'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]



