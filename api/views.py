# coding: utf-8
from django.shortcuts import render, HttpResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import StepUsers, StepUsersHistory
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import time


@csrf_exempt
def api_login(request):
    response_date = {}
    if (request.method == 'POST'):
        username = request.POST.get('user', '')
        password =request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
               response_date['test'] = "Успешно"
               login(request, user)
            # Redirect to a success page.
            else:
                response_date['error'] = "аккаунт отключен"
                return HttpResponse(json.dumps(response_date), content_type="application/json", status=422)
            # Return a 'disabled account' error message
        else:
            response_date['error'] = "Пароль или логин неверный"
            return HttpResponse(json.dumps(response_date), content_type="application/json", status=422)
        us = User.objects.get(username=username)
        use = StepUsers.objects.get(stepUser__username=username)
        response_date['first_name'] = us.getfirstname()
        response_date['last_name'] = us.getlastname()
        response_date['age'] = use.getage()
        response_date['city'] = use.getcity()
        response_date['allsteps'] = use.getsteps()
        response_date['photo'] = use.getphotourl()
        dt = date.today()
        usid = use.getid()
        ol = StepUsersHistory.objects.filter(user__id=usid).filter(date=dt)
        if ol.count() > 0:
            response_date['step'] = StepUsersHistory.objects.filter(user__id=usid).get(date=dt).getsteps()
        else:
            response_date['step'] = 0
    return HttpResponse(json.dumps(response_date), content_type="application/json", status=200)

@csrf_exempt
def api_reg(request):
    response_date = {}
    if (request.method == 'POST'):
        username = request.POST.get('user', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        us = User.objects.filter(username=username).values()
        if len(us) > 0:
            response_date['error'] = "Пользователь с таким ником уже существует"
            return HttpResponse(json.dumps(response_date), content_type="application/json")#, status_code=422)
        else:
            user = User.objects.create_user(username, 'lennon@thebeatles.com', password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            response_date['test'] = "Успешно"
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)
            userid = User.objects.get(username=username).getuser()
            uss = User.objects.get(pk=userid)
            stepuser = StepUsers(age=0, city="", steps=0)
            stepuser.stepUser=uss
            stepuser.save()
            us = User.objects.get(username=username)
            use = StepUsers.objects.get(stepUser__username=username)
            response_date['first_name'] = us.getfirstname()
            response_date['last_name'] = us.getlastname()
            response_date['age'] = use.getage()
            response_date['city'] = use.getcity()
            response_date['allsteps'] = use.getsteps()
            response_date['photo'] = use.getphotourl()
            dt = date.today()
            usid = use.getid()
            ol = StepUsersHistory.objects.filter(user__id=usid).filter(date=dt)
            if ol.count() > 0:
                response_date['step'] = StepUsersHistory.objects.filter(user__id=usid).get(date=dt).getsteps()
            else:
                response_date['step'] = 0
    return HttpResponse(json.dumps(response_date), content_type="application/json", status=201)


@csrf_exempt
def step_update(request):
    response_date = {}
    dt = date.today()
    if (request.method == 'POST'):
        username = request.POST.get('user', '')
        password =request.POST.get('password', '')
        step = request.POST.get('step', '')
        username = username.encode()
        allstepsquery = StepUsers.objects.filter(stepUser__username=username)
        allsteps = StepUsers.objects.get(stepUser__username=username).getsteps()
        usid = StepUsers.objects.get(stepUser__username=username).getid()
        history = StepUsersHistory.objects.filter(user__id=usid).filter(date=dt)
        if history.count() < 1:
            allsteps = int(step) + allsteps
            allstepsquery.update(steps=allsteps)
            stepuser = StepUsers.objects.get(stepUser__username=username)
            hist = StepUsersHistory(steps=step, date=dt)
            hist.user = stepuser
            hist.save()
        else:
            tod = StepUsersHistory.objects.filter(date=dt)
            if tod.count() < 1:
                allsteps = int(step) + allsteps
                allstepsquery.update(steps=allsteps)
                stepuser = StepUsers.objects.get(stepUser__username=username)
                hist = StepUsersHistory(steps=step, date=dt)
                hist.user = stepuser
                hist.save()
            else:
                allsteps = int(step) + allsteps
                allstepsquery.update(steps=allsteps)
                step = int(step) + StepUsersHistory.objects.filter(user__id=usid).get(date=dt).getsteps()
                history.update(steps=step)

    response_date['error'] = "Успешно"
    return HttpResponse(json.dumps(response_date), content_type="application/json", status=200)


@csrf_exempt
def api_info_update(request):
    response_date = {}
    if (request.method == 'POST'):
        username = request.POST.get('user', '')
        password =request.POST.get('password', '')
        # user = authenticate(username=username, password=password)
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        age = request.POST.get('age', '')
        city = request.POST.get('city', '')
        us = User.objects.filter(username=username)
        use = StepUsers.objects.filter(stepUser__username=username)
        if len(first_name) > 0:
            us.update(first_name=first_name)
        if len(last_name) > 0:
            us.update(last_name=last_name)
        if len(age) > 0:
            use.update(age=age)
        if len(city) > 0:
            use.update(city=city)
    response_date['error'] = "Успешно"
    return HttpResponse(json.dumps(response_date), content_type="application/json", status=200)


@csrf_exempt
def api_info(request):
    dt = date.today()
    response_date = {}
    if (request.method == 'POST'):
        username = request.POST.get('user', '')
        password = request.POST.get('password', '')
        us = User.objects.get(username=username)
        response_date['first_name'] = us.getfirstname()
        response_date['last_name'] = us.getlastname()
        use = StepUsers.objects.get(stepUser__username=username)
        response_date['age'] = use.getage()
        response_date['city'] = use.getcity()
        response_date['allsteps'] = use.getsteps()
        response_date['photo'] = use.getphotourl()
        usid = use.getid()
        ol = StepUsersHistory.objects.filter(user__id=usid).filter(date=dt)
        if ol.count() > 0:
            response_date['step'] = StepUsersHistory.objects.filter(user__id=usid).get(date=dt).getsteps()
        else:
            response_date['step'] = 0
        # return HttpResponse(json.dumps(response_date), content_type="application/json", status_code=422)
    # response_date['error'] = "Успешно"
    return HttpResponse(json.dumps(response_date), content_type="application/json")


@csrf_exempt
def history(request):
    s = []
    if (request.method == 'POST'):
        username = request.POST.get('user', '')
        password =request.POST.get('password', '')
        usid = StepUsers.objects.get(stepUser__username=username).getid()
        steps = StepUsersHistory.objects.filter(user__id=usid)
        for step in steps:
            b = {}
            st = step.getsteps()
            dt = step.getdate()
            dat = int(time.mktime(dt.timetuple())*1000)

            b['date'] = dat
            b['step'] = st
            s.append(b)
    return HttpResponse(json.dumps(s), content_type="application/json", status=200)

