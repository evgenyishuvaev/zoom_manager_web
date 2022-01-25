# Generated by Django 4.0.1 on 2022-01-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZoomCredentionals',
            fields=[
                ('name_data', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('data', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'zoom_credentionals',
            },
        ),
        migrations.CreateModel(
            name='ZoomMeetings',
            fields=[
                ('uuid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('host_id', models.CharField(max_length=255)),
                ('topic', models.CharField(max_length=255)),
                ('start_time', models.CharField(max_length=255)),
                ('duration', models.IntegerField()),
                ('type', models.IntegerField()),
                ('join_url', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'zoom_meetings',
            },
        ),
        migrations.CreateModel(
            name='ZoomUsers',
            fields=[
                ('host_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'zoom_users',
            },
        ),
    ]
