# Generated by Django 5.1.2 on 2024-11-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0035_remove_ecompromotiondiscountvariant_promo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecompromotiondiscountvariant',
            name='discount_type',
            field=models.IntegerField(choices=[(0, '%'), (1, 'k')]),
        ),
    ]