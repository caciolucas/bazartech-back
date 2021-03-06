# Generated by Django 3.2.9 on 2022-05-04 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.TextField()),
                ("description", models.TextField()),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="store.product")),
            ],
        ),
    ]
