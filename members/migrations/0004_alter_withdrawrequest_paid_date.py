# Generated by Django 3.2.20 on 2023-07-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20230727_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawrequest',
            name='paid_date',
            field=models.DateField(blank=True),
        ),
    ]
