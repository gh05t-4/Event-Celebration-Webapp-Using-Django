# Generated by Django 4.2.4 on 2023-08-10 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventCelebration', '0005_delete_presentationevents'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentationEvents',
            fields=[
                ('event_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('presentations_id', models.BigIntegerField()),
                ('event_name', models.CharField(max_length=50)),
                ('event_type', models.CharField(max_length=50)),
                ('event_end_date', models.DateField()),
                ('event_img', models.CharField(max_length=200)),
                ('event_description', models.CharField(max_length=280)),
            ],
        ),
    ]
