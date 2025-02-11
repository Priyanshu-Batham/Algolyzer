# Generated by Django 5.1.4 on 2025-02-11 04:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="course",
            field=models.CharField(default="Undecided", max_length=100),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="enrollment_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="full_name",
            field=models.CharField(default="Unknown", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userprofile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
