# Generated by Django 3.0.3 on 2020-04-16 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xmasg', '0006_auto_20200416_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='extraction_done',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
