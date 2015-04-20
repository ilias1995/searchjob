# coding: utf-8
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username




class JobType(models.Model):
    job_type = models.CharField(max_length=200)

    def __unicode__(self):
        return self.job_type

class Towns_and_regoins(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(User)
    name_town = models.ForeignKey(Towns_and_regoins, verbose_name="города и регионы: ")
    jobtype = models.ForeignKey(JobType, verbose_name="Вид работы: ")
    name_job = models.CharField(max_length=200, verbose_name="Название работы: ")
    how_many = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Количество работников: ")
    phone_number = models.IntegerField(verbose_name="Номер вашего телефона: ")
    email = models.EmailField()
    date_job = models.DateTimeField('Время добовление работы: ', default=datetime.now, blank=True)
    about = models.TextField(verbose_name="Какие требование к работе: ")

    def __unicode__(self):
        return self.name_job


class Pravila(models.Model):
    privetstvie = models.TextField()
    pravila_sayta = models.TextField()


