# Generated by Django 3.0.12 on 2021-02-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210214_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='demo_id',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='demo_id',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]