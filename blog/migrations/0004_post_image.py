# Generated by Django 5.0.2 on 2024-02-21 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_delete_publishedmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='blog/%Y/%m/%d'),
        ),
    ]
