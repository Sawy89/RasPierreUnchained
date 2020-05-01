# Generated by Django 3.0.3 on 2020-04-16 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xmasg', '0004_room_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='roommember',
            name='receiver',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='XmasGift',
        ),
    ]
