# Generated by Django 2.1.5 on 2019-02-23 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0007_auto_20190223_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetdetails',
            name='posted_by',
            field=models.CharField(default='', max_length=512),
        ),
    ]
