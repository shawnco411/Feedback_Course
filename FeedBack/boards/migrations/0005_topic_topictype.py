# Generated by Django 2.1.7 on 2019-05-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_post_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='topictype',
            field=models.CharField(default='', max_length=64, null=True),
        ),
    ]