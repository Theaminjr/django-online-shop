# Generated by Django 4.2.6 on 2023-10-18 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_category_parent_alter_productimage_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]