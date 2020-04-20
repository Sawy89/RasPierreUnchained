# Generated by Django 3.0.3 on 2020-04-16 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xmasg', '0005_auto_20200416_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roommember',
            name='receiver',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]