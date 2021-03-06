# Generated by Django 4.0.4 on 2022-05-18 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان دسته بندی')),
                ('name', models.CharField(max_length=100, verbose_name='نام دستبندی')),
                ('meta_description', models.TextField(max_length=200, verbose_name='متاتگ')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='پیوند یکتا')),
                ('status', models.BooleanField(default=True, verbose_name='منتشر شود؟')),
                ('position', models.IntegerField(verbose_name='پوزیشن')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان کتاب')),
                ('metadescription', models.TextField(max_length=200, verbose_name='متاتگ')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='پیوند یکتا')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='نام کتاب ')),
                ('image', models.FileField(blank=True, default='Unknown.jpg', upload_to='product/books/', verbose_name='تصویر')),
                ('price', models.PositiveBigIntegerField(verbose_name='قیمت')),
                ('status', models.BooleanField(default=True, verbose_name='منتشر شود؟')),
                ('inventory', models.PositiveBigIntegerField(verbose_name='تعداد موجودی')),
                ('properties', models.CharField(default=None, max_length=24, null=True)),
                ('description', models.TextField(max_length=500, verbose_name='توضیحات کتاب')),
                ('Category', models.ManyToManyField(blank=True, null=True, related_name='books', to='product.category', verbose_name='دستبندی')),
            ],
            options={
                'verbose_name': 'کتاب',
                'verbose_name_plural': 'کتاب ها',
            },
        ),
    ]
