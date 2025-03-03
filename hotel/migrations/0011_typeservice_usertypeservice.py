# Generated by Django 3.2.3 on 2021-06-04 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0010_auto_20210601_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('avg_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('user', models.ManyToManyField(blank=True, related_name='rated_services', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сервис',
                'verbose_name_plural': 'Сервисы',
            },
        ),
        migrations.CreateModel(
            name='UserTypeService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField()),
                ('type_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_type_service', to='hotel.typeservice')),
                ('user', models.ForeignKey(default=3, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='rated_type_service', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'type_service')},
            },
        ),
    ]
