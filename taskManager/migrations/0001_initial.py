# Generated by Django 3.2.6 on 2021-08-17 07:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Project title must be greater than 1 character')])),
                ('description', models.CharField(max_length=2000, validators=[django.core.validators.MinLengthValidator(2, 'Project description must be greater than 1 character')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Task title must be greater than 1 character')])),
                ('description', models.CharField(max_length=2000, validators=[django.core.validators.MinLengthValidator(2, 'Project description must be greater than 1 character')])),
                ('status', models.IntegerField(choices=[(1, 'Started'), (2, 'Processing'), (3, 'Pending'), (4, 'Ended')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskManager.project')),
            ],
        ),
    ]
