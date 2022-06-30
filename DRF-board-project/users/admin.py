from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile as ProfileModel


# 관리자 페이지 User 탭의 해당 유저 페이지에서 해당 유저의 프로필도 같이 볼 수 있도록 커스터마이징.
class ProfileInline(admin.StackedInline):
    model = ProfileModel
    can_delete = False
    verbose_name_plural = 'profile'
    
    
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
