# Generated by Django 5.1.2 on 2024-11-20 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0036_alter_ecompromotiondiscountvariant_discount_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EcomProductPromotionJoinTable',
            new_name='EcomProductPromotionExtra',
        ),
        migrations.AlterModelOptions(
            name='ecomproductpromotionextra',
            options={'verbose_name': 'Product Promotion Extra Info', 'verbose_name_plural': 'Product Promotion Extra Info'},
        ),
        migrations.AlterModelTable(
            name='ecomproductpromotionextra',
            table='ecom_product_promotion_extra',
        ),
    ]