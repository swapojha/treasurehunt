from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout
from hunt.models import LoggedInUser, GameUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.contrib import messages

# Create your views here.
def login_view(request,msg=''):
    if request.user.is_authenticated:
        # print(request.session['session_key'])
        return homepage_view(request)
    else:
        return render(request,'login.html',{'msg':msg})

def rules(request):
    return render(request,'rules.html')

def leaderboard(request):
    # Based on authentication
    number_of_top_user = 50
    game_users = GameUser.objects.filter(user__is_staff=False).order_by('-level','-score','timestamp')
    top_50 = game_users[:number_of_top_user]
    with_uid_self_user = None
    if request.user.is_authenticated:
        ranking = request.user.game_user.ranking()
        # with_uid_self_user = []
        # with_uid_self_user.append({
        #     'ranking':ranking,
        #     'guser':request.user.game_user,
        #     'uid':request.user.social_auth.get(provider='facebook').uid
        # })
        if ranking > number_of_top_user:
            with_uid_self_user = []
            with_uid_self_user.append({
                'ranking':ranking,
                'guser':request.user.game_user,
                'uid':request.user.social_auth.get(provider='facebook').uid
            })   
    with_uid_game_users = []
    for game_user in top_50:
        with_uid_game_users.append({
            'guser':game_user,
            'uid':game_user.user.social_auth.get(provider='facebook').uid,
        })
    return render(request,'leaderboard.html',{'top_50':with_uid_game_users,'self_user':with_uid_self_user})

def homepage_view(request):
    if request.user.is_authenticated:
        msg = 'You are logged in!'
        #print("Back here")
        LoggedInUser.objects.get_or_create(user = request.user)
        game_user = GameUser.objects.get(user = request.user)
        if game_user.blocked:
            messages.info(request,'Due to unfair play, your account has been blocked.')
            return logout_view(request)
        else:
            stored_session_key = request.user.logged_in_user.session_key
            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            #print(stored_session_key)
            if stored_session_key and stored_session_key != request.session.session_key:
                # print("Found Previous login")
                Session.objects.get(session_key=stored_session_key).delete()
            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()
            # social = request.user.social_auth.get(provider='facebook')
            # userid = social.uid
            return HttpResponseRedirect('/hunt')
    else:
        messages.info(request, 'You need to login first.')
        return HttpResponseRedirect('/')

def logout_view(request):
    if request.user.is_authenticated:
        LoggedInUser.objects.filter(user_id = request.user).delete()
        logout(request)
    return HttpResponseRedirect('/')