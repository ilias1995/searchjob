# coding: utf-8
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


class Job(models.Model):
    user = models.ForeignKey(User)
    name_town = models.CharField(max_length=200, verbose_name="Название города: ")
    jobtype = models.ForeignKey(JobType, verbose_name="Вид работы: ")
    name_job = models.CharField(max_length=200, verbose_name="Название работы: ")
    how_many = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Количество работников: ")
    email = models.EmailField()
    about = models.TextField(verbose_name="Какие требование к работе: ")

    def __unicode__(self):
        return self.name_job


class Pravila(models.Model):
    privetstvie = models.TextField()
    pravila_sayta = models.TextField()


