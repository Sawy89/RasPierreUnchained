# Generated by Django 3.0.7 on 2020-06-15 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alldoc', '0004_auto_20200615_2131'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='station',
            unique_together={('name', 'location')},
        ),
    ]