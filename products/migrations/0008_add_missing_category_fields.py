# Generated manually to add missing category fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_add_missing_product_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories/'),
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]



