# Generated by Django 4.0.4 on 2022-05-24 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='properties',
            new_name='auther_name',
        ),
    ]