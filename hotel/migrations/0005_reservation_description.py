# Generated by Django 3.2.3 on 2021-05-25 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_auto_20210525_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
