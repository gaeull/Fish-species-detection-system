# Generated by Django 4.1 on 2023-02-27 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fish', '0007_rename_end_date_fish_end_date2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fish',
            old_name='end_date2',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='fish',
            old_name='start_date2',
            new_name='start_date',
        ),
    ]
