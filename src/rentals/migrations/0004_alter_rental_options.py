# Generated by Django 5.0.4 on 2024-05-25 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_alter_rental_return_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rental',
            options={'ordering': ('-created',)},
        ),
    ]
