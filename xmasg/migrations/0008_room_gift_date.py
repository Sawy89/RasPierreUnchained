# Generated by Django 3.0.3 on 2020-04-20 15:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('xmasg', '0007_room_extraction_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='gift_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 20, 15, 32, 6, 645461, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
