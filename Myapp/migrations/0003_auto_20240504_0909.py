# Generated by Django 2.1.7 on 2024-05-04 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0002_auto_20240504_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesreport',
            name='CUSTOMER',
        ),
        migrations.RemoveField(
            model_name='salesreport',
            name='PRODUCT',
        ),
        migrations.RemoveField(
            model_name='salesreport',
            name='SELLER',
        ),
        migrations.DeleteModel(
            name='salesreport',
        ),
    ]
