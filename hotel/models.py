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
    room_class = models.CharField(max_length=10, choices=ROOM_CLASS, db_index=True)

    def __str__(self):
        return "Номер №{}".format(self.number)

    class Meta:
        verbose_name_plural = 'Номера'
        verbose_name = 'Номер'