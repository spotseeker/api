# Generated by Django 4.2.14 on 2024-11-24 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_postcomment_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postimage',
            unique_together={('post', 'order')},
        ),
    ]
