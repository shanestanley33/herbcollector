# Generated by Django 4.2.6 on 2023-11-01 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Watering Date')),
                ('water', models.CharField(choices=[('M', 'Monday'), ('F', 'Friday')], default='M', max_length=1)),
                ('herb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.herb')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
