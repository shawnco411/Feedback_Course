# Generated by Django 2.1.7 on 2019-06-04 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20190524_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='myfile',
            field=models.FileField(null=True, upload_to='%Y/%m/%d/'),
        ),
    ]
