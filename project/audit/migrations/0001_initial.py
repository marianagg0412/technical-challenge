# Generated by Django 5.1.3 on 2024-11-25 05:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.role')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('assigned_auditor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='controls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DesignQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_required', models.BooleanField(default=True)),
                ('control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='audit.control')),
            ],
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design_score', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('En proceso', 'En proceso'), ('Terminado', 'Terminado'), ('Sin iniciar', 'Sin iniciar'), ('No evaluado', 'No evaluado')], max_length=20)),
                ('date_elaborated', models.DateField(blank=True, null=True)),
                ('control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='validations', to='audit.control')),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='validations', to='audit.cycle')),
            ],
        ),
        migrations.CreateModel(
            name='DesignAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='audit.designquestion')),
                ('validation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='audit.validation')),
            ],
        ),
    ]