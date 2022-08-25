# Generated by Django 4.0.4 on 2022-08-25 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tapp1', '0002_createstockgrp'),
    ]

    operations = [
        migrations.CreateModel(
            name='group_summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('alias', models.CharField(max_length=100, null=True)),
                ('under', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(max_length=100, null=True)),
                ('units', models.CharField(max_length=100, null=True)),
                ('batches', models.CharField(max_length=100, null=True)),
                ('manufacturing_date', models.CharField(max_length=100, null=True)),
                ('expiry_dates', models.CharField(max_length=100, null=True)),
                ('rate_of_duty', models.CharField(max_length=100, null=True)),
                ('quantity', models.CharField(max_length=100, null=True)),
                ('rate', models.CharField(max_length=100, null=True)),
                ('per', models.CharField(max_length=100, null=True)),
                ('value', models.CharField(max_length=100, null=True)),
                ('additional', models.CharField(max_length=100, null=True)),
                ('CreateStockGrp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tapp1.createstockgrp')),
            ],
        ),
    ]