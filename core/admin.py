from django.contrib import admin

from core.models import *


@admin.register(User)
class User(admin.ModelAdmin):
    fields = ['password', 'last_login', 'is_superuser', 'username',
              'first_name', 'last_name', 'email', 'is_staff', 'is_active',
              'date_joined', 'profile_pic', 'address', 'home_phone', 'my_phone',
              'links', 'birthday_date', 'graduate', 'employer']


@admin.register(Graduate)
class Graduate(admin.ModelAdmin):
    fields = ['education', 'work_experience']


@admin.register(Employer)
class Employer(admin.ModelAdmin):
    fields = ['company_name', 'work_area', 'image']


@admin.register(Resume)
class Resume(admin.ModelAdmin):
    fields = ['graduate', 'description', 'work_experience']


@admin.register(Vacancy)
class Vacancy(admin.ModelAdmin):
    fields = ['employer', 'profession', 'demands', 'description']
