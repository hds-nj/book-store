# Generated by Django 4.0.4 on 2022-05-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_alter_profile_birth_date_alter_profile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='نام'),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='نام خانوادگی'),
        ),
    ]