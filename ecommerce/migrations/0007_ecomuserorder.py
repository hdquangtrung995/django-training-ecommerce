# Generated by Django 5.1.2 on 2024-10-29 13:22

import django.db.models.deletion
import model_utils.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_alter_ecomproductpromotionjointable_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EcomUserOrder',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_status', models.CharField(choices=[(0, 'in progress'), (1, 'check out'), (2, 'placed'), (3, 'complete'), (4, 'canceled')], default=0)),
                ('total_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping_address', models.CharField(max_length=300)),
                ('shipping_city', models.CharField(max_length=100)),
                ('placed_at', models.DateField(blank=True, null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'db_table': 'ecom_user_order',
            },
        ),
    ]