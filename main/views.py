# coding:utf8
from datetime import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import ProfileEditForm
from .models import StepUsers, StepUsersHistory


def testy(request):
    return render(request, 'test.html')


def index(request):
    return render(request, 'index.html')


def step_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile(request, user.id)
                return redirect('profile', user.id)
            # Redirect to a success page.
        #     else:
        #         response_date['error'] = "аккаунт отключен"
        #         return HttpResponse(json.dumps(response_date), content_type="application/json", status=422)
        #     # Return a 'disabled account' error message
        # else:
        #     response_date['error'] = "Пароль или логин неверный"
        #     return HttpResponse(json.dumps(response_date), content_type="application/json", status=422)
        # us = User.objects.get(username=username)
        # use = StepUsers.objects.get(stepUser__username=username)
        # response_date['first_name'] = us.getfirstname()
        # response_date['last_name'] = us.getlastname()
        # response_date['age'] = use.getage()
        # response_date['city'] = use.getcity()
        # response_date['allsteps'] = use.getsteps()
        # response_date['photo'] = use.getphotourl()
        # dt = date.today()
        # usid = use.getid()
        # ol = StepUsersHistory.objects.filter(user__id=usid).filter(date=dt)
        # if ol.count() > 0:
        #     response_date['step'] = StepUsersHistory.objects.filter(user__id=usid).get(date=dt).getsteps()
        # else:
        #     response_date['step'] = 0
    return redirect('index')


def step_logout(request):
    logout(request)
    return redirect('index')


def profile(request, user_id):
    users = StepUsers.objects.all().order_by('-steps')[:10]
    usersteps = StepUsersHistory.objects.all()
    theUser = StepUsers.objects.get(stepUser__id=user_id)
    fats = StepUsers.objects.all().order_by('steps')[:10]

    month = date.today() - timedelta(days=30)
    week = date.today() - timedelta(days=7)
    today = date.today()

    stepsmonth = StepUsersHistory.objects.filter(user__stepUser__id=user_id).filter(date__range=(month, today))
    stepmonth = 0
    for step in stepsmonth:
        stepmonth += step.steps

    stepsweek = StepUsersHistory.objects.filter(user__stepUser__id=user_id).filter(date__range=(week, today))
    stepweek = 0
    for step in stepsweek:
        stepweek += step.steps

    stepstoday = StepUsersHistory.objects.filter(user__stepUser__id=user_id).filter(date=today)
    steptoday = 0
    for step in stepstoday:
        steptoday += step.steps

    allsteps = StepUsersHistory.objects.filter(user__stepUser__id=user_id)
    allstep = 0
    for step in allsteps:
        allstep += step.steps

    context = {
        'theUser': theUser,
        'users': users,
        'usersteps': usersteps,
        'fats': fats,
        'stepmonth': stepmonth,
        'stepweek': stepweek,
        'steptoday': steptoday,
        'allstep': allstep
    }
    return render(request, 'profile/profile.html', context)


def profile_edit(request, user_id, ):
    theUser = StepUsers.objects.get(stepUser__id=user_id)
    context = {
        'theUser': theUser
    }
    return render(request, 'profile/profile-edit.html', context)


def profile_edit_form(request, user_id):
    form = ProfileEditForm()
    if request.method == 'POST':
        f = ProfileEditForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        age = request.POST['age']
        if f.is_valid():
            StepUsers.objects.filter(stepUser=user_id).update(city=city, age=age)
            User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name)
            use = StepUsers.objects.get(stepUser=user_id)
            use.photo = request.FILES['photo']
            use.save()
            return redirect('profile', user_id)
        context = {
            'form': f,
            'first_name': first_name,
            'last_name': last_name,
            'city': city,
            'age': age
        }
        return render(request, 'profile/profile-edit.html', context)
    return redirect('profile_edit')


def profiles(request):
    users = StepUsers.objects.all()
    steps = StepUsersHistory.objects.all()
    context = {
        'users': users,
        'steps': steps
    }
    return render(request, 'profile/profiles.html', context)
