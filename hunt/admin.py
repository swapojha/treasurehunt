from django.contrib import admin
from .models import LoggedInUser, GameUser,GameUserData,Question,Hint
# Register your models here.

admin.site.register(LoggedInUser)
admin.site.register(GameUser)
admin.site.register(GameUserData)
admin.site.register(Question)
admin.site.register(Hint)