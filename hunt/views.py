from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout
from .models import LoggedInUser, Question, GameUserData, GameUser, Hint
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.utils import timezone
from .forms import answer_form
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
import random

first_bonus_limit=30
second_bonus_limit=40
first_bonus_penalty=19
second_bonus_penalty=29

def get_bonus_hints(player):
    # first_bonus_limit=600
    # second_bonus_limit=1200
    user = player.game_user
    quest = Question.objects.get(level = player.game_user.level)
    user_question_data = GameUserData.objects.get(game_user=user,question=quest)
    st_time = user_question_data.start_time
    time_delta = timezone.now()-st_time
    diff_in_minutes = time_delta.total_seconds()/60
    hints = Hint.objects.get(question = quest)
    bonus_hints = None
    if diff_in_minutes > second_bonus_limit:
        if not user_question_data.hint_5_used:
            bonus_hints = {
                'show':[],
                'hide':['first']
            }
        else:
            bonus_hints = {
                'show':[hints.hint_5],
                'hide':[]
            }
        if not user_question_data.hint_6_used:
            bonus_hints['hide'].append('second')
        else:
            bonus_hints['show'].append(hints.hint_6)
    elif diff_in_minutes > first_bonus_limit:
        if not user_question_data.hint_5_used:
            bonus_hints = {
                'show':[],
                'hide':['first']
            }
        else:
            bonus_hints = {
                'show':[hints.hint_5],
                'hide':[]
            }
    return bonus_hints

def available_hints(request):
    first_hint_time = 5
    second_hint_time = 10
    third_hint_time = 15
    fourth_hint_time = 20
    custom_info = 'No more hints available as of now.'
    hints_finished_info = 'No more hints available for this question'
    user = request.user.game_user
    quest = Question.objects.get(level = request.user.game_user.level)
    user_question_data = GameUserData.objects.get(game_user=user,question=quest)
    hints = Hint.objects.get(question = quest)
    st_time = user_question_data.start_time
    time_delta = timezone.now()-st_time
    diff_in_minutes = time_delta.total_seconds()/60
    hint_array = {
        'hints':[],
        'custom_info':custom_info,
    }
    if diff_in_minutes > fourth_hint_time:
        #show first four hints
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2,hints.hint_3,hints.hint_4],
            'custom_info':hints_finished_info,
        }
        user_question_data.hint_used = 4
    elif diff_in_minutes > third_hint_time:
        #show first three hints
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2,hints.hint_3],
            'custom_info':custom_info,
        }
        user_question_data.hint_used = 3
    elif diff_in_minutes > second_hint_time:
        #show first two hints
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2],
            'custom_info':custom_info,
        }
        user_question_data.hint_used = 2
    elif diff_in_minutes > first_hint_time:
        #show first hint
        hint_array = {
            'hints':[hints.hint_1],
            'custom_info':custom_info,
        }
        user_question_data.hint_used = 1
    user_question_data.save()
    return JsonResponse(hint_array)

def update_question_score(player_question_data):
    print("Score updation")
    deduction_limit_one = 5
    score_deduct_one = 5
    deduction_limit_two = 10
    score_deduct_two = 7
    deduction_limit_three = 15
    score_deduct_three = 11
    st_time = player_question_data.start_time
    time_delta = timezone.now()-st_time
    diff_in_minutes = time_delta.total_seconds()/60
    print("Difference: ",diff_in_minutes)
    if diff_in_minutes > deduction_limit_three:
        player_question_data.score -= score_deduct_three
    elif  diff_in_minutes > deduction_limit_two:
        player_question_data.score -= score_deduct_two
    elif diff_in_minutes > deduction_limit_one:
        player_question_data.score -= score_deduct_one
    print(player_question_data.score)
    print("Score updations ends")
    player_question_data.save()


def check_timeout(game_user):
    time_limit = 120
    no_of_attempts = 20
    if(game_user.last_attempt):
        attempts = game_user.timeout_attempts
        last_attempt =  game_user.last_attempt
        time_delta = timezone.now()-last_attempt
        diff_in_seconds = time_delta.total_seconds()
        if diff_in_seconds < time_limit:
            attempts += 1
            game_user.timeout_attempts = attempts
            game_user.save()
            if attempts > no_of_attempts:
                return True
            else:
                return False
        else:
            game_user.last_attempt = timezone.now()
            game_user.timeout_attempts = 0
            game_user.save()
            return False
    else:
        game_user.last_attempt = timezone.now()
        game_user.timeout_attempts = 0
        game_user.save()
        return False

def get_random_success_message():
    msg = ["Right answer", "Nice try, right answer","Right answer, well done"]
    return random.randint(0,len(msg)-1)

def get_random_error_message():
    msg = ["Wrong answer", "Better luck next time","Keep trying, you can do it. Wrong answer."]
    return random.randint(0,len(msg)-1)

# Create your views here.
class hunt_view(object):
    def index(request):
        if request.user.is_authenticated:
            user_timed_out = check_timeout(request.user.game_user)
            if user_timed_out:
                firstname = request.user.first_name
                user_level = request.user.game_user.level
                return render(request,'hunt/timed_out.html',{'username':firstname, 'level':user_level})
            else:
                if request.method == 'POST':
                    form = answer_form(request.POST)
                    if form.is_valid():
                        current_user = request.user
                        quest = Question.objects.get(level = request.user.game_user.level)
                        user_question_data = GameUserData.objects.get(game_user=current_user.game_user,question=quest)
                        user_question_data.attempts += 1
                        user_question_data.save()
                        given_answer = form.cleaned_data['answer']
                        valid_answer = Question.objects.get(level = request.user.game_user.level).answer
                        if valid_answer == given_answer:
                            quest.sattempts+=1
                            quest.save()
                            print("Updating score of question")
                            update_question_score(user_question_data)
                            user_question_data.end_time = timezone.now()
                            user_question_data.save()
                            current_user.game_user.levelup(user_question_data.score,timezone.now(),user_question_data.attempts)
                            current_user.game_user.save()
                            try:
                                next_quest = Question.objects.get(level = request.user.game_user.level)
                                GameUserData.objects.create(game_user=current_user.game_user,question=next_quest,start_time=timezone.now(),score=next_quest.score)
                            except ObjectDoesNotExist:
                                pass
                            messages.success(request, get_random_success_message())
                        else:
                            messages.error(request, get_random_error_message())
                        return HttpResponseRedirect('/hunt')
                elif request.is_ajax():
                    return available_hints(request)
                else:
                    # social = request.user.social_auth.get(provider='facebook')
                    # userid = social.uid
                    firstname = request.user.first_name
                    user_level = request.user.game_user.level
                    try:
                        question = Question.objects.get(level = user_level)
                        form = answer_form()
                        bonus_data = get_bonus_hints(request.user)
                        return render(request,'hunt/home.html', {'username':firstname, 'level':user_level , 'question':question , 'form': form,'bonus':bonus_data})
                    except ObjectDoesNotExist:
                        return render(request,'hunt/success.html',{'username':firstname})
        else:
            messages.info(request, 'You need to login first.')
            return HttpResponseRedirect('/')

    # def get_hint(request):
    #     if request.user.is_authenticated:
    #         #Check time elapsed on this question.Depending on time elapsed send appropriate number of hints to the user
    #         #First four hints have no score deduction
    #         #Next four hints will have score deduction
    #         return available_hints(request)
    #     else:
    #         messages.info(request, 'You need to login first.')
    #         return HttpResponseRedirect('/')

    def get_bonus_hint(request):
        if request.user.is_authenticated:
            user = request.user.game_user
            quest = Question.objects.get(level = request.user.game_user.level)
            user_question_data = GameUserData.objects.get(game_user=user,question=quest)
            hints = Hint.objects.get(question = quest)
            st_time = user_question_data.start_time
            time_delta = timezone.now()-st_time
            diff_in_minutes = time_delta.total_seconds()/60
            hint_id = request.GET.get('id','')
            hint_data = {
                'hint':[],
            }
            if hint_id == 'first' and diff_in_minutes > first_bonus_limit:
                hint_data = {
                    'hint': [hints.hint_5],
                }
                user_question_data.hint_5_used = True
                user_question_data.score -= first_bonus_penalty
                user_question_data.save()
                hints.save()
            elif hint_id == 'second' and diff_in_minutes > second_bonus_limit:
                hint_data = {
                    'hint': [hints.hint_6],
                }
                user_question_data.hint_6_used = True
                user_question_data.score -= second_bonus_penalty
                user_question_data.save()
                hints.save()
            return JsonResponse(hint_data)
        else:
            messages.info(request, 'You need to login first.')
            return HttpResponseRedirect('/')


class admin_view(object):
    def index(request):
        pass