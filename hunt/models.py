from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
# Create your models here.

# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user',on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username

class GameUser(models.Model):
    user = models.OneToOneField(User, related_name="game_user",on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)
    blocked = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(null=True)
    total_attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(default=timezone.now())
    timeout_attempts = models.IntegerField(0)
    def levelup(self,ques_score,timestamp,attempts):
        self.level+=1
        self.score+=ques_score
        self.timestamp=timestamp
        self.total_attempts+=attempts

class Question(models.Model):
    level = models.PositiveSmallIntegerField(default=1)
    link = models.CharField(max_length=200,null=True,blank=True)
    ques_type = models.CharField(max_length=10,null=True,blank=True)
    score = models.IntegerField(default=0)
    answer = models.CharField(max_length=100,null=True,blank=True)
    sattempts = models.IntegerField(default=0)
    
class Hint(models.Model):
    question = models.OneToOneField(Question, related_name='question_hint',on_delete=models.CASCADE)
    no_of_hints = models.IntegerField(default=0)
    hint_1 = models.CharField(max_length=100,null=True,blank=True)
    hint_2 = models.CharField(max_length=100,null=True,blank=True)
    hint_3 = models.CharField(max_length=100,null=True,blank=True)
    hint_4 = models.CharField(max_length=100,null=True,blank=True)
    hint_5 = models.CharField(max_length=100,null=True,blank=True)
    hint_6 = models.CharField(max_length=100,null=True,blank=True)
    hint_7 = models.CharField(max_length=100,null=True,blank=True)
    hint_8 = models.CharField(max_length=100,null=True,blank=True)

class GameUserData(models.Model):
    game_user = models.ForeignKey(GameUser, related_name='game_user_data',on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='on_question',on_delete=models.CASCADE)
    hint_used = models.PositiveSmallIntegerField(default=0)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    feed = models.CharField(max_length=1000,null=True,blank=True)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    hint_5_used = models.BooleanField(default=False)
    hint_6_used = models.BooleanField(default=False)
    hint_7_used = models.BooleanField(default=False)
    hint_8_used = models.BooleanField(default=False)   

from .receiver import *