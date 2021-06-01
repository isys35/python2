# Generated by Django 3.2.3 on 2021-06-01 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0009_alter_room_number_of_rooms'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('reservation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hotel.reservation')),
            ],
            options={
                'verbose_name': 'Заселение',
                'verbose_name_plural': 'Заселения',
            },
            bases=('hotel.reservation',),
        ),
        migrations.AlterField(
            model_name='room',
            name='number_of_rooms',
            field=models.PositiveIntegerField(choices=[(2, 2), (3, 3), (4, 4)], db_index=True, verbose_name='Кол-во комнат'),
        ),
    ]
