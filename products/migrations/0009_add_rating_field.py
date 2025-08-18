# Generated manually to add rating field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_add_missing_category_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]


