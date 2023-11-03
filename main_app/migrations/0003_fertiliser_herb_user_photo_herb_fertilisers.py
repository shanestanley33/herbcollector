# Generated by Django 4.2.6 on 2023-11-03 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0002_watering'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fertiliser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='herb',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('herb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.herb')),
            ],
        ),
        migrations.AddField(
            model_name='herb',
            name='fertilisers',
            field=models.ManyToManyField(to='main_app.fertiliser'),
        ),
    ]
