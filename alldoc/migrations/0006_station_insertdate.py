# Generated by Django 3.0.7 on 2020-06-18 15:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alldoc', '0005_auto_20200615_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='insertdate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
