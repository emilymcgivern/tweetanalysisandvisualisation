# Generated by Django 2.1.7 on 2019-02-28 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0021_tweetreplies_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('userid', models.CharField(default='', max_length=512)),
                ('screen_name', models.CharField(default='', max_length=512)),
                ('followers_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='reaction',
            name='sentiment_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tweetreplies',
            name='sentiment_value',
            field=models.IntegerField(default=0),
        ),
    ]
