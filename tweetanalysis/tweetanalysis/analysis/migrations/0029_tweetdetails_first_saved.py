from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0028_auto_20190228_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetdetails',
            name='first_saved',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
