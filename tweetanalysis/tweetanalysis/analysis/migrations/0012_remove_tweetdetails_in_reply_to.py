# Generated by Django 2.1.5 on 2019-02-23 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0011_tweetdetails_in_reply_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetdetails',
            name='in_reply_to',
        ),
    ]
