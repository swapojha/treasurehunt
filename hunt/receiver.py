from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone 
from .models import GameUser, Question, GameUserData


@receiver(post_save, sender=User)
def make_player_profile(sender, instance, created, **kwargs):
      if created:
          game_user = GameUser.objects.create(user=instance)
          level = 1
          quest = Question.objects.get(level=level)
          GameUserData.objects.create(game_user = game_user, question = quest,start_time = timezone.now(),score = quest.score)
