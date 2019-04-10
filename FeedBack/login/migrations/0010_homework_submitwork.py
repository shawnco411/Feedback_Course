# Generated by Django 2.1.7 on 2019-04-10 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20190406_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('content', models.CharField(max_length=512)),
                ('deadline', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework', to='login.course')),
            ],
        ),
        migrations.CreateModel(
            name='SubmitWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit', models.CharField(max_length=1000)),
                ('submit_time', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_sub', to='login.User')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submit', to='login.Homework')),
            ],
        ),
    ]