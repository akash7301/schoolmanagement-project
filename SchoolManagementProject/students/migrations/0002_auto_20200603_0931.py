# Generated by Django 3.0.6 on 2020-06-03 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='current_status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='surname',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
