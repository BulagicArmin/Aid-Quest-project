# Generated by Django 3.0.6 on 2020-05-17 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('naziv', models.CharField(default='New User', max_length=255)),
                ('predstavnik', models.CharField(blank=True, max_length=255)),
                ('skr_naziv', models.CharField(blank=True, max_length=55)),
                ('reg_ured', models.CharField(blank=True, max_length=255)),
                ('sjediste', models.CharField(blank=True, max_length=255)),
                ('tel_num', phonenumber_field.modelfields.PhoneNumberField(default='+387', max_length=128, region=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Donator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('full_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Datum rodjenja')),
                ('adress', models.CharField(blank=True, max_length=255)),
                ('tel_num', phonenumber_field.modelfields.PhoneNumberField(default='+387', max_length=128, region=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
