# Generated by Django 3.0.3 on 2020-05-17 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myself', '0002_auto_20200517_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='language',
            field=models.CharField(default='it', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='content',
            name='name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterUniqueTogether(
            name='content',
            unique_together={('name', 'language')},
        ),
    ]