# Generated by Django 3.1.6 on 2021-04-15 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0007_transaction_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='donate.user'),
        ),
    ]
