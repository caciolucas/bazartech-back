# Generated by Django 3.2.9 on 2022-05-07 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_user_registered_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.TextField(blank=True, default="QmXBdsBBD6cpXuFg9fCWrpQBhLmntHyLwh3EgvPHVP8UxL", null=True),
        ),
    ]
