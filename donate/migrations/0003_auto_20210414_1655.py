# Generated by Django 3.1.6 on 2021-04-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0002_organization_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.TextField(blank=True),
        ),
    ]