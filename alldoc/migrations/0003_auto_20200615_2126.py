# Generated by Django 3.0.7 on 2020-06-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alldoc', '0002_auto_20200615_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='description',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
