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

# first_bonus_limit=30
# second_bonus_limit=40
# first_bonus_penalty=19
# second_bonus_penalty=29

# def get_bonus_hints(player):
#     # first_bonus_limit=600
#     # second_bonus_limit=1200
#     user = player.game_user
#     quest = Question.objects.get(level = player.game_user.level)
#     user_question_data = GameUserData.objects.get(game_user=user,question=quest)
#     st_time = user_question_data.start_time
#     time_delta = timezone.now()-st_time
#     diff_in_minutes = time_delta.total_seconds()/60
#     hints = Hint.objects.get(question = quest)
#     bonus_hints = None
#     if diff_in_minutes > second_bonus_limit:
#         if not user_question_data.hint_5_used:
#             bonus_hints = {
#                 'show':[],
#                 'hide':['first']
#             }
#         else:
#             bonus_hints = {
#                 'show':[hints.hint_5],
#                 'hide':[]
#             }
#         if not user_question_data.hint_6_used:
#             bonus_hints['hide'].append('second')
#         else:
#             bonus_hints['show'].append(hints.hint_6)
#     elif diff_in_minutes > first_bonus_limit:
#         if not user_question_data.hint_5_used:
#             bonus_hints = {
#                 'show':[],
#                 'hide':['first']
#             }
#         else:
#             bonus_hints = {
#                 'show':[hints.hint_5],
#                 'hide':[]
#             }
#     return bonus_hints


def get_custom_hints_message(curr_slot,no_of_hints):
    custom_info = 'No more hints available as of now.'
    hints_finished_info = 'No more hints available for this question'
    if curr_slot < no_of_hints:
        return custom_info
    else:
        return hints_finished_info

def available_hints(request):
    first_hint_time = 10
    second_hint_time = 20
    third_hint_time = 30
    fourth_hint_time = 40
    fifth_hint_time = 50
    sixth_hint_time = 60
    seventh_hint_time = 70
    custom_info = 'No more hints available as of now.'
    hints_finished_info = 'No more hints available for this question'
    user = request.user.game_user
    quest = Question.objects.get(level = request.user.game_user.level)
    user_question_data = GameUserData.objects.get(game_user=user,question=quest)
    hints = Hint.objects.get(question = quest)
    no_of_hints = hints.no_of_hints
    st_time = user_question_data.start_time
    time_delta = timezone.now()-st_time
    diff_in_minutes = time_delta.total_seconds()/60
    hint_array = {
        'hints':[],
        'custom_info':'No hints avaliable as of now',
    }
    if diff_in_minutes > seventh_hint_time:
        #show first four hints
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2,hints.hint_3,hints.hint_4,hints.hint_5,hints.hint_6,hints.hint_7],
            'custom_info':hints_finished_info,
        }
        user_question_data.hint_used = 7
    elif diff_in_minutes > sixth_hint_time:
        #show first four hints
        to_show_info = get_custom_hints_message(6,no_of_hints)
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2,hints.hint_3,hints.hint_4,hints.hint_5,hints.hint_6],
            'custom_info':to_show_info,
        }
        user_question_data.hint_used = 6
    elif diff_in_minutes > fifth_hint_time:
        #show first four hints
        to_show_info = get_custom_hints_message(5,no_of_hints)
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2,hints.hint_3,hints.hint_4,hints.hint_5],
            'custom_info':to_show_info,
        }
        user_question_data.hint_used = 5
    elif diff_in_minutes > fourth_hint_time:
        #show first four hints
        to_show_info = get_custom_hints_message(4,no_of_hints)
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2,hints.hint_3,hints.hint_4],
            'custom_info':to_show_info,
        }
        user_question_data.hint_used = 4
    elif diff_in_minutes > third_hint_time:
        #show first three hints
        to_show_info = get_custom_hints_message(3,no_of_hints)
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2,hints.hint_3],
            'custom_info':to_show_info,
        }
        user_question_data.hint_used = 3
    elif diff_in_minutes > second_hint_time:
        #show first two hints
        to_show_info = get_custom_hints_message(2,no_of_hints)
        hint_array = {
            'hints':[hints.hint_1,hints.hint_2],
            'custom_info':to_show_info,
        }
        user_question_data.hint_used = 2
    elif diff_in_minutes > first_hint_time:
        #show first hint
        to_show_info = get_custom_hints_message(1,no_of_hints)
        hint_array = {
            'hints':[hints.hint_1],
            'custom_info':to_show_info,
        }
        user_question_data.hint_used = 1
    user_question_data.save()
    return JsonResponse(hint_array)

def update_question_score(player_question_data,sattempts):
    """
        Before:
        This was to update the score of the user on the basis of time he took to solve the question.
    """
    # # print("Score updation")
    # deduction_limit_one = 5
    # score_deduct_one = 5
    # deduction_limit_two = 10
    # score_deduct_two = 7
    # deduction_limit_three = 15
    # score_deduct_three = 11
    # st_time = player_question_data.start_time
    # time_delta = timezone.now()-st_time
    # diff_in_minutes = time_delta.total_seconds()/60
    # # print("Difference: ",diff_in_minutes)
    # if diff_in_minutes > deduction_limit_three:
    #     player_question_data.score -= score_deduct_three
    # elif  diff_in_minutes > deduction_limit_two:
    #     player_question_data.score -= score_deduct_two
    # elif diff_in_minutes > deduction_limit_one:
    #     player_question_data.score -= score_deduct_one
    # # print(player_question_data.score)
    # # print("Score updations ends")
    # player_question_data.save()
    """
        Now:
        No deduction on the basis of time he/she took.
        We will deduct marks on the basis of how many people have solved this question before him/her.
    """
    deduction_limit_one = 15
    score_deduct_one = 3
    deduction_limit_two = 30
    score_deduct_two = 6
    deduction_limit_three = 45
    score_deduct_three = 8
    if sattempts > deduction_limit_three:
        player_question_data.score -= score_deduct_three
    elif sattempts > deduction_limit_two:
        player_question_data.score -= score_deduct_two
    elif sattempts > deduction_limit_one:
        player_question_data.score -= score_deduct_one
    player_question_data.save()

def check_timeout(game_user):
    time_limit = 120
    no_of_attempts = 40
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
    return msg[random.randint(0,len(msg)-1)]

def get_random_error_message():
    msg = ["Wrong answer", "Better luck next time","Keep trying, you can do it. Wrong answer."]
    return msg[random.randint(0,len(msg)-1)]

def clean_answer(answer):
    if not answer:
        return ''
    cleaned=''
    for letter in answer:
        if letter>='a' and letter <='z':
            cleaned+=letter
        elif letter >='A' and letter <='Z':
            cleaned+=letter
        elif letter >='0' and letter <='9':
            cleaned+=letter
        elif letter != ' ':
            cleaned+=answer
    cleaned = cleaned.lower()
    return cleaned

# Create your views here.
class hunt_view(object):
    def index(request):
        if request.user.is_authenticated:
            game_user = GameUser.objects.get(user = request.user)
            if game_user.blocked:
                return HttpResponseRedirect('/')
            user_timed_out = check_timeout(request.user.game_user)
            if user_timed_out:
                firstname = request.user.first_name
                user_level = request.user.game_user.level
                return render(request,'hunt/timed_out.html',{'username':firstname, 'level':user_level})
            else:
                # if request.method == 'POST':
                #     # return HttpResponse("Boom")
                #     print(request.POST)
                #     form = answer_form(request.POST)
                #     if form.is_valid():
                #         current_user = request.user
                #         quest = Question.objects.get(level = request.user.game_user.level)
                #         user_question_data = GameUserData.objects.get(game_user=current_user.game_user,question=quest)
                #         user_question_data.attempts += 1
                #         user_question_data.save()
                #         given_answer = form.cleaned_data['answer']
                #         #given the input in form we need to convert it into compressed form
                #         #i.e no spaces and all lowercase for comparison with correct answer
                #         given_answer = clean_answer(given_answer)
                #         if len(given_answer) > 50:
                #             given_answer = given_answer[:50]
                #         # return HttpResponse("Boom")
                #         #save  whatever user gave as input into feed
                #         #only going to store last 15 inputs
                #         feed = (user_question_data.feed)
                #         if feed:
                #             count = feed.count(' ')
                #             if(count>=15):
                #                 pos = feed.find(' ')
                #                 feed = feed[pos+1:]
                #             feed += given_answer
                #             feed += ' '
                #         else:
                #             feed = given_answer+' '
                #         user_question_data.feed = feed
                #         user_question_data.save()
                #         #end saving
                #         valid_answer = Question.objects.get(level = request.user.game_user.level).answer
                #         if valid_answer == given_answer:
                #             quest.sattempts+=1
                #             quest.save()
                #             # print("Updating score of question")
                #             update_question_score(user_question_data,quest.sattempts)
                #             user_question_data.end_time = timezone.now()
                #             user_question_data.save()
                #             current_user.game_user.levelup(user_question_data.score,timezone.now(),user_question_data.attempts)
                #             current_user.game_user.save()
                #             try:
                #                 next_quest = Question.objects.get(level = request.user.game_user.level)
                #                 GameUserData.objects.create(game_user=current_user.game_user,question=next_quest,start_time=timezone.now(),score=next_quest.score)
                #             except ObjectDoesNotExist:
                #                 pass
                #             messages.success(request, get_random_success_message())
                #         else:
                #             messages.error(request, get_random_error_message())
                #         return HttpResponseRedirect('/hunt')
                #     else:
                #         messages.error(request, get_random_error_message())
                #         return HttpResponseRedirect('/hunt')
                # # elif request.is_ajax():
                # #     return available_hints(request)
                # else:
                    # social = request.user.social_auth.get(provider='facebook')
                    # userid = social.uid
                firstname = request.user.first_name
                user_level = request.user.game_user.level
                try:
                    question = Question.objects.get(level = user_level)
                    form = answer_form()
                    #bonus_data = get_bonus_hints(request.user)
                    return render(request,'hunt/home.html', {'username':firstname, 'level':user_level , 'question':question , 'form': form})
                    #return render(request,'hunt/home.html', {'username':firstname, 'level':user_level , 'question':question , 'form': form,'bonus':bonus_data})
                except ObjectDoesNotExist:
                    return render(request,'hunt/success.html',{'username':firstname})
        else:
            messages.info(request, 'You need to login first.')
            return HttpResponseRedirect('/')

    def check_answer(request):
        if request.user.is_authenticated:
            if request.method == "POST":
                game_user = GameUser.objects.get(user = request.user)
                if game_user.blocked:
                    user_data = {
                        'blocked' : True
                    }
                    return JsonResponse(user_data)
                user_timed_out = check_timeout(request.user.game_user)
                if user_timed_out:
                    firstname = request.user.first_name
                    user_level = request.user.game_user.level
                    user_data = {
                        'blocked' : False,
                        'timeout' : True,
                    }
                    return JsonResponse(user_data)
                    # return render(request,'hunt/timed_out.html',{'username':firstname, 'level':user_level})
                else:
                    form = answer_form(request.POST)
                    #return JsonResponse({'hell':False})
                    if form.is_valid():
                        #return JsonResponse({'kam':False})
                        current_user = request.user
                        quest = Question.objects.get(level = request.user.game_user.level)
                        user_question_data = GameUserData.objects.get(game_user=current_user.game_user,question=quest)
                        user_question_data.attempts += 1
                        user_question_data.save()
                        given_answer = form.cleaned_data['answer']
                        #given the input in form we need to convert it into compressed form
                        #i.e no spaces and all lowercase for comparison with correct answer
                        given_answer = clean_answer(given_answer)
                        if len(given_answer) > 50:
                            given_answer = given_answer[:50]
                        # return HttpResponse("Boom")
                        #save  whatever user gave as input into feed
                        #only going to store last 15 inputs
                        feed = (user_question_data.feed)
                        if feed:
                            count = feed.count(' ')
                            if(count>=15):
                                pos = feed.find(' ')
                                feed = feed[pos+1:]
                            feed += given_answer
                            feed += ' '
                        else:
                            feed = given_answer+' '
                        user_question_data.feed = feed
                        user_question_data.save()
                        #end saving
                        valid_answer = Question.objects.get(level = request.user.game_user.level).answer
                        user_data = {
                            'success' : None,
                            'error' : None,
                            'img_link' : None,
                            'level': None
                        }
                        if valid_answer == given_answer:
                            quest.sattempts+=1
                            quest.save()
                            # print("Updating score of question")
                            update_question_score(user_question_data,quest.sattempts)
                            user_question_data.end_time = timezone.now()
                            user_question_data.save()
                            current_user.game_user.levelup(user_question_data.score,timezone.now(),user_question_data.attempts)
                            current_user.game_user.save()
                            try:
                                next_quest = Question.objects.get(level = request.user.game_user.level)
                                GameUserData.objects.create(game_user=current_user.game_user,question=next_quest,start_time=timezone.now(),score=next_quest.score)
                                user_data['img_link'] = next_quest.link
                                user_data['level'] = next_quest.level
                            except ObjectDoesNotExist:
                                pass
                            user_data['success'] = get_random_success_message()
                            #messages.success(request, get_random_success_message())
                        else:
                            #return JsonResponse({'bam':False})
                            user_data['error'] = get_random_error_message()
                            #messages.error(request, get_random_error_message())
                        return JsonResponse(user_data)
                    else:
                        user_data = {
                            'success' : None,
                            'error' : None,
                            'img_link' : None,
                            'level': None
                        }
                        user_data['error'] = get_random_error_message()
                        return JsonResponse(user_data)    
                        # messages.error(request, get_random_error_message())
                        # return HttpResponseRedirect('/hunt')
            else:
                messages.info(request, 'Invalid url')    
                return HttpResponseRedirect('/')    
        else:
            messages.info(request, 'You need to login first.')    
            return HttpResponseRedirect('/')

    def get_hint(request):
        if request.user.is_authenticated:
            #Check time elapsed on this question.Depending on time elapsed send appropriate number of hints to the user
            #First four hints have no score deduction
            #Next four hints will have score deduction
            return available_hints(request)
        else:
            messages.info(request, 'You need to login first.')
            return HttpResponseRedirect('/')

    # def get_bonus_hint(request):
    #     if request.user.is_authenticated:
    #         user = request.user.game_user
    #         quest = Question.objects.get(level = request.user.game_user.level)
    #         user_question_data = GameUserData.objects.get(game_user=user,question=quest)
    #         hints = Hint.objects.get(question = quest)
    #         st_time = user_question_data.start_time
    #         time_delta = timezone.now()-st_time
    #         diff_in_minutes = time_delta.total_seconds()/60
    #         hint_id = request.GET.get('id','')
    #         hint_data = {
    #             'hint':[],
    #         }
    #         if hint_id == 'first' and diff_in_minutes > first_bonus_limit:
    #             hint_data = {
    #                 'hint': [hints.hint_5],
    #             }
    #             user_question_data.hint_5_used = True
    #             user_question_data.score -= first_bonus_penalty
    #             user_question_data.save()
    #             hints.save()
    #         elif hint_id == 'second' and diff_in_minutes > second_bonus_limit:
    #             hint_data = {
    #                 'hint': [hints.hint_6],
    #             }
    #             user_question_data.hint_6_used = True
    #             user_question_data.score -= second_bonus_penalty
    #             user_question_data.save()
    #             hints.save()
    #         return JsonResponse(hint_data)
    #     else:
    #         messages.info(request, 'You need to login first.')
    #         return HttpResponseRedirect('/')


class admin_view(object):
    def index(request):
        pass