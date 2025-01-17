# Generated by Django 5.1 on 2024-09-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='arrival_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_arrived',
            field=models.BooleanField(default=False),
        ),
    ]
