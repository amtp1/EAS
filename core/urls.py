from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core.views import *

urlpatterns = [
    path('', index, name='index'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/signup', signup, name='signup'),
    path('accounts/logout', account_logout, name='account_logout'),
    path('profile/<str:username>/', profile_info, name='profile_info'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('profile/add_resume', add_resume, name='add_resume')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
