# Generated by Django 3.2.2 on 2021-05-12 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolver', '0005_mxrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='mxrecord',
            name='record_name',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]