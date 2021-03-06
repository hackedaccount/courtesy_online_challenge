from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model

import datetime
import os


# User = get_user_model()


def get_upload_path(instance, filename):
    return os.path.join(
        "%s" % instance.module.module_number, filename)


class Module(models.Model):
    module_number = models.IntegerField()
    module_name = models.CharField(max_length=50)

    def __str__(self):
        return self.module_name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    level = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    random_number = models.IntegerField(default=1)
    timestamp = models.DateTimeField()
    player_emotion = models.CharField(max_length=50, default='neutral', blank=True, null=True)
    video_viewed = models.IntegerField(default=0)
    base_module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True, default='images/level1.jpg')
    videofile = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    audiofile = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    question = models.TextField(null=True, blank=True)
    option1 = models.TextField(null=True, blank=True)
    option2 = models.TextField(null=True, blank=True)
    numuser = models.IntegerField(default=0)
    option1_level_score = models.IntegerField(default=0)
    option2_level_score = models.IntegerField(default=0)

    # accuracy = models.FloatField(default=0)
    wrong = models.IntegerField(default=0)

    def __str__(self):
        return '- '.join([str(self.module), self.question])

    class Meta:
        ordering = ['-pk']


class Answer(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    facial_expression = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '- '.join([self.user.name, str(self.question.module), self.question.question])


class Notif(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Emotion(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    emotion = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return '- '.join([self.user.name, self.emotion])
