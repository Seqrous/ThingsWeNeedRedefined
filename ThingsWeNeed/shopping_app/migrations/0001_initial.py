# Generated by Django 3.0.7 on 2020-07-16 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('postal_code', models.CharField(max_length=10)),
                ('street_address', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('street_address', 'city', 'country')},
            },
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='shopping_app.Address')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('max_price', models.FloatField(blank=True)),
                ('quantity', models.PositiveIntegerField()),
                ('info', models.TextField(blank=True, max_length=256)),
                ('is_wish', models.BooleanField()),
                ('bought_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shopping_app.Household')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='household', to='shopping_app.Household')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='household',
            name='members',
            field=models.ManyToManyField(through='shopping_app.HouseholdMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
