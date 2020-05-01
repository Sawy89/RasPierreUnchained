# Generated by Django 3.0.3 on 2020-04-01 06:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('admin', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
