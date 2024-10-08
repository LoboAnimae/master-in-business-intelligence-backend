# Generated by Django 5.1 on 2024-08-15 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=152)),
            ],
        ),
        migrations.CreateModel(
            name='HourDayMonthLatency',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField()),
                ('day_of_month_id', models.IntegerField()),
                ('latency', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='HourDayWeekLatency',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField()),
                ('day_of_week_id', models.IntegerField()),
                ('latency', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='SimultaneousJobsDayWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField()),
                ('day_of_month_id', models.IntegerField()),
                ('amount_jobs_done', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('scheme', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='backend.scheme')),
            ],
        ),
        migrations.CreateModel(
            name='TableMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('mean_st', models.FloatField()),
                ('std_st', models.FloatField()),
                ('min', models.FloatField()),
                ('max', models.FloatField()),
                ('initial_range', models.FloatField()),
                ('final_range', models.FloatField()),
                ('table_response_size', models.FloatField()),
                ('scheme', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='backend.scheme')),
                ('table', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='backend.table')),
            ],
        ),
    ]
