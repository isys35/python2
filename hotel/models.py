from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    ROOM_CLASS = [
        ('ECN', 'Эконом'),
        ('STD', 'Стандарт'),
        ('VIP', 'VIP'),
    ]
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер комнаты")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    number_of_rooms = models.PositiveIntegerField(verbose_name='Кол-во комнат', db_index=True)
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    room_class = models.CharField(max_length=10, choices=ROOM_CLASS, db_index=True, verbose_name='Класс номера')

    def __str__(self):
        return "Номер №{}".format(self.number)

    class Meta:
        verbose_name_plural = 'Номера'
        verbose_name = 'Номер'


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Номер')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    # TODO: Сделать валидацию по времемени(started_at>now, ended_at>started_at)
    description = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Брони'
        verbose_name = 'Бронь'

    def __str__(self):
        return "Бронь пользователя {}".format(self.user.username)