from django.db import models


class Room(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер комнаты")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    number_of_rooms = models.PositiveIntegerField(verbose_name='Кол-во комнат')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')