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
    return HttpResponse('Rules page')

def leaderboard(request):
    # No need for user authentication
    game_users = GameUser.objects.filter(user__is_staff=False).order_by('score')
    with_uid_game_users = []
    for game_user in game_users:
        with_uid_game_users.append({
            'guser':game_user,
            'uid':game_user.user.social_auth.get(provider='facebook').uid,
        })
    return render(request,'leaderboard.html',{'gameusers':with_uid_game_users})

def homepage_view(request):
    if request.user.is_authenticated:
        msg = 'You are logged in!'
        #print("Back here")
        LoggedInUser.objects.get_or_create(user = request.user)
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