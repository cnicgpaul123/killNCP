# Generated by Django 2.1.7 on 2020-02-20 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personinfo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personinfo',
            name='travel_mode',
            field=models.IntegerField(blank=True, choices=[(1, '火车'), (2, '自驾'), (3, '汽车'), (4, '飞机')], help_text='春运出行方式', null=True, verbose_name='春运出行方式'),
        ),
    ]
