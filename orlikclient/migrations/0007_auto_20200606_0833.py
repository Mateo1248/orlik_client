# Generated by Django 3.0.6 on 2020-06-06 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orlikclient', '0006_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(),
        ),
    ]
