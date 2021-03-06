# Generated by Django 3.2.9 on 2022-05-07 01:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_auto_20220506_2233"),
        ("authentication", "0004_alter_user_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="common.address",
                verbose_name="Address",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="birthdate",
            field=models.DateField(blank=True, null=True, verbose_name="Birthdate"),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name="Gender"),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="Ativo",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether the user can log into this admin site.",
                verbose_name="Staff",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=255, verbose_name="User"),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name="User"),
        ),
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.TextField(
                blank=True,
                default="QmXBdsBBD6cpXuFg9fCWrpQBhLmntHyLwh3EgvPHVP8UxL",
                null=True,
                verbose_name="Profile picture",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="registered_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Registered at"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=255, unique=True, verbose_name="User"),
        ),
    ]
