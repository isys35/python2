from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    ROOM_CLASS = [
        ('ECN', 'Эконом'),
        ('STD', 'Стандарт'),
        ('VIP', 'VIP'),
    ]
    ROOMS_COUNT = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    ]
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер комнаты")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    number_of_rooms = models.PositiveIntegerField(verbose_name='Кол-во комнат',
                                                  choices=ROOMS_COUNT,
                                                  db_index=True)
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    room_class = models.CharField(max_length=10,
                                  choices=ROOM_CLASS,
                                  db_index=True,
                                  verbose_name='Класс номера')

    def __str__(self):
        return "Номер №{}".format(self.number)

    class Meta:
        verbose_name_plural = 'Номера'
        verbose_name = 'Номер'


class Message(models.Model):
    text = models.TextField(db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Пользователь',
                               related_name='messages')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = 'Сообщение'
        ordering = ['pub_date']


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             verbose_name='Номер',
                             related_name="booked")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    description = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Брони'
        verbose_name = 'Бронь'

    def __str__(self):
        return "Бронь комнаты {} пользователем {}".format(self.room, self.user.username)


class CheckIn(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             verbose_name='Номер',
                             related_name="check_ins")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    last_message_today = models.ForeignKey(Message,
                                           on_delete=models.SET_NULL,
                                           blank=True,
                                           null=True,
                                           verbose_name='Последнее сообщение за сегодня'
                                           )

    class Meta:
        verbose_name_plural = 'Заселения'
        verbose_name = 'Заселение'

    def __str__(self):
        return "Жизнь в {} пользователем {}".format(self.room, self.user.username)


class TypeService(models.Model):
    title = models.CharField(max_length=50)
    avg_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )
    count_rate = models.IntegerField(null=False, blank=False, default=0)
    users = models.ManyToManyField(
        User,
        related_name="rated_services",
        through="UserTypeService",
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Сервисы'
        verbose_name = 'Сервис'


class UserTypeService(models.Model):
    class Meta:
        unique_together = ("user", "type_service")
        verbose_name_plural = 'Оценки'
        verbose_name = 'Оценка'

    user = models.ForeignKey(
        User,
        related_name="rated_type_service",
        on_delete=models.CASCADE,
    )
    type_service = models.ForeignKey(
        TypeService,
        on_delete=models.CASCADE,
        related_name="rated_type_service"
    )
    rate = models.PositiveSmallIntegerField()
