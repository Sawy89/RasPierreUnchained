# Generated by Django 3.0.3 on 2020-04-04 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xmasg', '0002_auto_20200404_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='admin',
        ),
        migrations.AddField(
            model_name='roommember',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
