from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('',hunt_view.index,name='hunt_view'),
    path('hint',hunt_view.get_hint,name='hint_view'),
    path('answer',hunt_view.check_answer,name="answer_view")
    # path('nimda_control/',admin_view.index,name='admin_view'),
    # path('bonus_hint/',hunt_view.get_bonus_hint,name='bonus_hint_view')
    # path('get_hint/',hunt_view.get_hint,name='hint_view')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)