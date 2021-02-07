# Generated by Django 3.0.12 on 2021-02-07 00:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210206_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsuser',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
        ),
    ]
