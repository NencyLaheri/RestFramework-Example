
from wsgiref.validate import validator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core import validators

class StudentModel(models.Model):
    name=models.CharField(max_length=100)
    roll=models.IntegerField()
    city=models.CharField(max_length=100)


# @receiver(post_save,sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender,instance=None,created=False,**kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Singer(models.Model):
    name=models.CharField(max_length=100)
    gender_choice=[('Male','Male'),('Female','Female')]
    gender=models.CharField(choices=gender_choice,max_length=20)

    def __str__(self):
        return self.name


class Song(models.Model):
    title=models.CharField(max_length=100)
    singer=models.ForeignKey(Singer,on_delete=models.CASCADE,related_name='song')
    duration=models.IntegerField(validators=[validators.MinValueValidator(1),validators.MaxValueValidator(10)])

    def __str__(self):
        return self.title