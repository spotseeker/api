# Generated by Django 4.2.14 on 2024-11-13 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='is_achived',
            new_name='is_archived',
        ),
    ]