# Generated by Django 2.2 on 2019-06-11 17:20

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20190610_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='img_url',
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
