# Generated by Django 2.2.6 on 2020-05-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsl', '0010_auto_20200506_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='update_version',
            name='status',
            field=models.CharField(default='1', max_length=128),
        ),
    ]
