# Generated by Django 3.0.3 on 2020-05-17 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myself', '0003_auto_20200517_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=128)),
                ('text_short', models.CharField(max_length=5000)),
                ('text_all', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.AddField(
            model_name='contents',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='myself.Languages'),
        ),
        migrations.AlterUniqueTogether(
            name='contents',
            unique_together={('name', 'language')},
        ),
    ]