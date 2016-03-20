# coding:utf8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class StepUser(models.Model):
    user = models.OneToOneField(User, verbose_name='Логин', null=True, blank=True, unique=True)
    age = models.IntegerField('Возраст', null=True, blank=True)
    city = models.CharField('Город', max_length=50, null=True, blank=True)
    photo = models.ImageField('Фото', upload_to='users/photo', null=True, blank=True)
    steps = models.BigIntegerField('Общее количество шагов', null=True, blank=True)

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    def get_name(self):
        if self.get_first_name() and self.get_last_name():
            return '%s %s' % (self.get_last_name(), self.get_first_name())
        else:
            return self.user.username

    def get_age(self):
        return self.age

    def get_city(self):
        return self.city

    def get_steps(self):
        return self.steps

    def get_photo_url(self):
        if self.photo:
            return self.photo.url

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class StepUserHistory(models.Model):
    step_user = models.ForeignKey(StepUser, verbose_name='Пользователь')
    date = models.DateTimeField('Дата')
    steps = models.BigIntegerField('Количество шагов')

    def get_steps(self):
        return self.steps

    def get_date(self):
        return self.date

    def __str__(self):
        return '%s %d' % (self.step_user.user.username, self.steps)

    class Meta:
        verbose_name = 'история пользователя'
        verbose_name_plural = 'истории пользователей'
