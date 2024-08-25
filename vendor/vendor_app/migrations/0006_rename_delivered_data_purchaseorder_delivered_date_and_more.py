# Generated by Django 5.0.4 on 2024-05-26 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor_app", "0005_rename_delivered_date_purchaseorder_delivered_data"),
    ]

    operations = [
        migrations.RenameField(
            model_name="purchaseorder",
            old_name="delivered_data",
            new_name="delivered_date",
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("completed", "Completed"),
                    ("canceled", "Canceled"),
                ],
                max_length=20,
            ),
        ),
    ]