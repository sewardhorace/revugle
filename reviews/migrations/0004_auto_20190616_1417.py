# Generated by Django 2.2 on 2019-06-16 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20190611_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='critic',
            name='slug',
            field=models.SlugField(default='default_slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='category',
            field=models.CharField(choices=[('', '--Category--'), ('BOOK', 'Books'), ('EVEN', 'Events'), ('MOVI', 'Movies'), ('MUSI', 'Music'), ('PLAC', 'Places'), ('PROD', 'Products'), ('TV', 'TV'), ('OTHE', 'Other')], default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='review',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_title'),
        ),
    ]