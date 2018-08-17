from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
from django.db.models import Count
from django.db.models.signals import post_init
# Create your models here.

# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user',on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return "User: "+self.user.username


class GameUser(models.Model):
    user = models.OneToOneField(User, related_name="game_user",on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)
    blocked = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(null=True)
    total_attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True)
    timeout_attempts = models.IntegerField(default=0)
    
    def levelup(self,ques_score,timestamp,attempts):
        self.level+=1
        self.score+=ques_score
        self.last_attempt=timestamp
        self.total_attempts+=attempts
    
    def ranking(self):
        rank_one = GameUser.objects.filter(user__is_staff=False,level__gt=self.level).count()
        rank_two = GameUser.objects.filter(user__is_staff=False,level=self.level,score__gt=self.score).count()
        rank_three = 0
        if self.level == 1:
            rank_three = GameUser.objects.filter(user__is_staff=False,level=self.level,score=self.score,timestamp__lt=self.timestamp).count()
        else:
            rank_three = GameUser.objects.filter(user__is_staff=False,level=self.level,score=self.score,last_attempt__lt=self.last_attempt).count()
        return rank_one + rank_two + rank_three + 1
    
    def __str__(self):
        return "User: "+str(self.user.username)+" Level: "+str(self.level)

def extraInitForMyModel(**kwargs):
    instance = kwargs.get('instance')
    if not instance.timestamp:
        instance.timestamp = timezone.now()

post_init.connect(extraInitForMyModel, GameUser)

class Question(models.Model):
    level = models.PositiveSmallIntegerField(default=1)
    link = models.CharField(max_length=200,null=True,blank=True)
    ques_type = models.CharField(max_length=10,null=True,blank=True)
    score = models.IntegerField(default=0)
    answer = models.CharField(max_length=50,null=True,blank=True)
    sattempts = models.IntegerField(default=0)
    def __str__(self):
        return "Level: "+str(self.level)
    
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
    def __str__(self):
        return "Level: "+str(self.question.level)

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
    def __str__(self):
        return "User: "+str(self.game_user.user.username)+" Level: "+str(self.question.level)   

from .receiver import *