# Generated by Django 4.2.17 on 2025-01-13 06:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_description', models.TextField(max_length=200)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to=product.models.upload_to, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('product_quantity', models.PositiveIntegerField()),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
