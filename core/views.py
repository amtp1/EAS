from datetime import datetime as dt

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from core.forms import UserCustomCreationForm
from core.models import *

@login_required(login_url='profile')
def index(request):
    if request.user.is_authenticated:
        return redirect('profile')


@login_required
def profile(request):
    vacancies = None
    if request.user.graduate:
        vacancies = Vacancy.objects.all()
    return render(request, 'profile.html', {'user': request.user, 'vacancies': vacancies})


@login_required
def profile_info(request, username):
    return render(request, 'profile_info.html', {'user': request.user})


def signup(request):
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCustomCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def edit_profile(request):
    post = request.POST
    user = User.objects.get(pk=request.user.id)
    for p in post:
        value = post.get(p)
        if value:
            if p == 'first_name':
                user.first_name = value
            elif p == 'last_name':
                user.last_name = value
            elif p == 'birthday_date':
                date = dt.strptime(value, '%d/%m/%Y')
                user.birthday_date = date
            elif p == 'address':
                user.address = value
            elif p == 'email':
                user.email = value
            elif p == 'my_phone':
                user.my_phone = value
            elif p == 'home_phone':
                user.home_phone = value
    user.save()
    return JsonResponse({'response': True})


def add_resume(request):
    user = User.objects.get(pk=request.user.id)
    description = request.POST.get('description')
    Resume.objects.create(graduate=user.graduate, description=description)
    return JsonResponse({'response': True})


def account_logout(request):
    logout(request)
    return redirect('index')
