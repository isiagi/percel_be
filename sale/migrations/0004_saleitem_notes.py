# Generated by Django 4.2.17 on 2025-01-22 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_alter_sale_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
