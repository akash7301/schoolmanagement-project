# Generated by Django 3.0.6 on 2020-05-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20200522_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='pic',
            field=models.ImageField(blank=True, default='default_user.png', upload_to=''),
        ),
    ]
