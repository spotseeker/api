# Generated by Django 4.2.14 on 2024-11-23 02:38

from django.db import migrations, models
import spotseeker.utils.otp


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userotp',
            name='otp',
            field=models.CharField(default=spotseeker.utils.otp.generate_otp, max_length=6, verbose_name='code for validations'),
        ),
    ]
