# Generated by Django 3.2.20 on 2023-07-27 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WithdrawDetail',
            new_name='WithdrawRequest',
        ),
        migrations.AlterModelOptions(
            name='withdrawrequest',
            options={'verbose_name': 'Withdraw Request', 'verbose_name_plural': 'Withdraw Requests'},
        ),
    ]
