# Generated by Django 2.2.6 on 2019-11-06 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsl', '0003_add_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_host',
            name='port',
            field=models.CharField(default=22, max_length=128, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='add_host',
            name='IP',
            field=models.CharField(default=22, max_length=128, unique=True),
        ),
    ]