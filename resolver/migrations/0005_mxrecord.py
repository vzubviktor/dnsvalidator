# Generated by Django 3.2.2 on 2021-05-12 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolver', '0004_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='MXrecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(max_length=1000)),
                ('domain', models.CharField(max_length=1000)),
            ],
        ),
    ]