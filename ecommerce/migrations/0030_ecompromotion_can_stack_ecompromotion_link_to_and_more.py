# Generated by Django 5.1.2 on 2024-11-19 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0029_rename_store_id_ecomstorebranch_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecompromotion',
            name='can_stack',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ecompromotion',
            name='link_to',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='ecompromotion',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ecompromotion',
            name='promotion_type',
            field=models.IntegerField(blank=True, choices=[(0, 'product'), (1, 'coupon'), (2, 'flash sale'), (3, 'free ship')], null=True),
        ),
        migrations.AlterField(
            model_name='ecompromotion',
            name='min_purchase',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]