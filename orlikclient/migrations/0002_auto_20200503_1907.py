# Generated by Django 3.0.5 on 2020-05-03 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orlikclient', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LoginData',
            new_name='RegisterData',
        ),
    ]