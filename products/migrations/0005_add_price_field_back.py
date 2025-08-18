# Generated manually to fix missing price field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20250814_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, default=0.00),
            preserve_default=False,
        ),
    ]



