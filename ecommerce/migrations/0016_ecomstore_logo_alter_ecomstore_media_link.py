# Generated by Django 5.1.2 on 2024-11-13 04:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ecommerce", "0015_ecomstore_banners_alter_ecomcategory_parent_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="ecomstore",
            name="logo",
            field=models.CharField(blank=True, null=True),
        ),
    ]
    # migrations.AlterField(
    #     model_name='ecomstore',
    #     name='media_link',
    #     field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(blank=True, null=True), default=list, size=None),
    # ),