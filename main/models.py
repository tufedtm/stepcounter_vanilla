# coding: utf8
from django.db import models
from django.contrib.auth.models import User


class StepUsers(models.Model):
    stepUser = models.ForeignKey(User, verbose_name='Пользователь', null=True, blank=True)
    age = models.IntegerField('Возраст', null=True, blank=True)
    city = models.CharField('Город', max_length=50, null=True, blank=True)
    photo = models.ImageField('Фото', upload_to='users/photo', null=True, blank=True)
    steps = models.BigIntegerField('Общее количество шагов', null=True, blank=True)

    def getphotourl(self):
        if len(str(self.photo)) > 0:
            return "http://127.0.0.1:8000/media/"+str(self.photo)
        return None

    def getsteps(self):
        return self.steps

    def getage(self):
        return self.age

    def getcity(self):
        return self.city

    def getid(self):
        return self.id

    def __unicode__(self):
        return unicode(self.stepUser)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class StepUsersHistory(models.Model):
    user = models.ForeignKey(StepUsers, verbose_name='Пользователь')
    date = models.DateField('Дата', auto_now_add=True)
    steps = models.BigIntegerField('Количество шагов')

    def getsteps(self):
        return self.steps

    def getdate(self):
        return self.date

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = 'история пользователя'
        verbose_name_plural = 'истории пользователей'