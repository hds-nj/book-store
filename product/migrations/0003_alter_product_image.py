# Generated by Django 4.0.4 on 2022-05-19 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, default='Unknown.jpg', upload_to='media/products', verbose_name='تصویر'),
        ),
    ]
