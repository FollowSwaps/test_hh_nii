# Generated by Django 3.2.6 on 2021-08-02 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='guid',
        ),
    ]
