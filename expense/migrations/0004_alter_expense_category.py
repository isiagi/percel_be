# Generated by Django 4.2.17 on 2025-01-22 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_expense_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
