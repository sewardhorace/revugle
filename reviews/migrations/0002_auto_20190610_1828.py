# Generated by Django 2.2 on 2019-06-10 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='group',
        ),
        migrations.AlterField(
            model_name='review',
            name='category',
            field=models.CharField(choices=[('MOVI', 'Movies'), ('TV', 'TV'), ('MUSI', 'Music'), ('BOOK', 'Books'), ('EVEN', 'Events'), ('PLAC', 'Places'), ('PROD', 'Products'), ('OTHE', 'Other')], default='OTHE', max_length=4),
        ),
        migrations.AlterField(
            model_name='review',
            name='img_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
