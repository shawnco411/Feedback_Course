# Generated by Django 2.1.7 on 2019-04-01 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_time',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]