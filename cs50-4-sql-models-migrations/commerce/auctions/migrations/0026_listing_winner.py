# Generated by Django 5.0.4 on 2024-05-04 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_rename_bid_bid_highest_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]