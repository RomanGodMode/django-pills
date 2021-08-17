from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


def pill_form_icon_path(instance, filename):
    return f'icons/{filename}'


class PillTaking(models.Model):
    class Meta:
        verbose_name = 'Приём препарата'
        verbose_name_plural = 'Приёмы препаратов'

    pill_course = models.ForeignKey('PillCourse', on_delete=CASCADE, verbose_name='Курс')
    time_taking = models.TimeField(verbose_name='Время принятия')
    is_took = models.BooleanField(default=False, verbose_name='Принято')

    # time_took = models.TimeField(null=True, verbose_name='Действительное время принятия')

    def __str__(self):
        return f'Курс ({self.pill_course}) приём - {self.time_taking}'


class PillForm(models.Model):
    class Meta:
        verbose_name = 'Вид препарата'
        verbose_name_plural = 'Виды препаратов'

    name = models.CharField(max_length=50, verbose_name='Название формы препарата')
    icon = models.FileField(upload_to=pill_form_icon_path, default='icons/default.png')

    def __str__(self):
        return self.name


class PillCurrency(models.Model):
    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    name = models.CharField(max_length=50, unique=True, verbose_name='Название единицы измерения')
    pill_form = models.ForeignKey(PillForm, on_delete=CASCADE, verbose_name='Форма приёма')
    abbreviation = models.CharField(max_length=10, verbose_name='Краткое название единицы измерения')

    def __str__(self):
        return self.name


class TakingIntervalType(models.Model):
    class Meta:
        verbose_name = 'Тип интервала'
        verbose_name_plural = 'Типы интервалов'

    title = models.CharField(max_length=50, verbose_name='Обозначение интервала')
    day_skip = models.PositiveIntegerField(verbose_name='Кол-во дней')

    def __str__(self):
        return self.title


class PillCourse(models.Model):
    class Meta:
        verbose_name = 'Курс препарата'
        verbose_name_plural = 'Курсы препаратов'

    TAKING_CONDITIONS_CHOICES = (
        (1, 'Перед едой'),
        (2, 'После еды'),
        (3, 'Натощак')
    )

    owner = models.ForeignKey(User, on_delete=CASCADE, verbose_name='Владелец')
    pill_name = models.CharField(max_length=50, unique=True, verbose_name='Название препарата')
    description = models.CharField(max_length=50, verbose_name='Описание')
    taking_condition = models.PositiveIntegerField(choices=TAKING_CONDITIONS_CHOICES, null=True,
                                                   verbose_name='Условие приёма')

    pill_form = models.ForeignKey(PillForm, on_delete=CASCADE, verbose_name='Вид препарата')
    pill_currency = models.ForeignKey(PillCurrency, on_delete=CASCADE, verbose_name='Единица измерения')
    single_dose = models.IntegerField(verbose_name='Разовая доза')
    taking_interval = models.ForeignKey(TakingIntervalType, on_delete=CASCADE, verbose_name='Интервал принятия')

    days_count = models.PositiveIntegerField(verbose_name='Кол-во дней в курсе')
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата конца', default=None, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.date_end = self.date_start + timedelta(days=self.days_count)
        super(PillCourse, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner.username} ({self.pill_name})'
