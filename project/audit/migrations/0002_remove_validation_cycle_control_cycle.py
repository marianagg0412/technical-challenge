# Generated by Django 5.1.3 on 2024-11-25 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='validation',
            name='cycle',
        ),
        migrations.AddField(
            model_name='control',
            name='cycle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='controls', to='audit.cycle'),
        ),
    ]