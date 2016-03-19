# coding:utf8
from __future__ import unicode_literals
import json
import time
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from main.models import StepUser, StepUserHistory


@csrf_exempt
def api_login(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
            else:
                response['error'] = 'Аккаунт отключен'

                return HttpResponse(json.dumps(response))
        else:
            response['error'] = 'Неверный логин или пароль'

            return HttpResponse(json.dumps(response))

        step_user = StepUser.objects.get(user__username=username)
        response['first_name'] = step_user.get_first_name()
        response['last_name'] = step_user.get_last_name()
        response['age'] = step_user.get_age()
        response['city'] = step_user.get_city()
        response['photo'] = step_user.get_photo_url()
        response['steps_all'] = step_user.get_steps()

        date = {
            'year': timezone.now().date().year,
            'month': timezone.now().date().month,
            'day': timezone.now().date().day
        }
        response['steps_today'] = sum(
            [x.steps for x in StepUserHistory.objects.filter(step_user__id=step_user.id).filter(
                date__year=date.get('year'),
                date__month=date.get('month'),
                date__day=date.get('day')
            )])

    return HttpResponse(json.dumps(response))


@csrf_exempt
def api_reg(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        try:
            StepUser.objects.get(user__username=username)
            response['error'] = 'Пользователь с таким логином уже существует'

            return HttpResponse(json.dumps(response))
        except StepUser.DoesNotExist:
            user = User(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            StepUser.objects.create(user_id=user.id)

            # auth_user = authenticate(username=username, password=password)
            # login(request, auth_user)

            response['first_name'] = first_name
            response['last_name'] = last_name
            response['age'] = 0
            response['city'] = ''
            response['photo'] = ''
            response['steps_all'] = 0
            response['steps_today'] = 0

    return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def step_update(request):
    response_date = {}
    dt = date.today()
    if request.method == 'POST':
        username = request.POST.get('user', '')
        password =request.POST.get('password', '')
        step = request.POST.get('step', '')
        username = username.encode()
        allstepsquery = StepUser.objects.filter(stepUser__username=username)
        allsteps = StepUser.objects.get(stepUser__username=username).getsteps()
        usid = StepUser.objects.get(stepUser__username=username).getid()
        history = StepUserHistory.objects.filter(user__id=usid).filter(date=dt)
        if history.count() < 1:
            allsteps = int(step) + allsteps
            allstepsquery.update(steps=allsteps)
            stepuser = StepUser.objects.get(stepUser__username=username)
            hist = StepUserHistory(steps=step, date=dt)
            hist.user = stepuser
            hist.save()
        else:
            tod = StepUserHistory.objects.filter(date=dt)
            if tod.count() < 1:
                allsteps = int(step) + allsteps
                allstepsquery.update(steps=allsteps)
                stepuser = StepUser.objects.get(stepUser__username=username)
                hist = StepUserHistory(steps=step, date=dt)
                hist.user = stepuser
                hist.save()
            else:
                allsteps = int(step) + allsteps
                allstepsquery.update(steps=allsteps)
                step = int(step) + StepUserHistory.objects.filter(user__id=usid).get(date=dt).getsteps()
                history.update(steps=step)

    response_date['error'] = "Успешно"
    return HttpResponse(json.dumps(response_date), content_type="application/json", status=200)


@csrf_exempt
def api_info_update(request):
    response_date = {}
    if request.method == 'POST':
        username = request.POST.get('user', '')
        password =request.POST.get('password', '')
        # user = authenticate(username=username, password=password)
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        age = request.POST.get('age', '')
        city = request.POST.get('city', '')
        us = User.objects.filter(username=username)
        use = StepUser.objects.filter(stepUser__username=username)
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
    if request.method == 'POST':
        username = request.POST.get('user', '')
        password = request.POST.get('password', '')
        us = User.objects.get(username=username)
        response_date['first_name'] = us.getfirstname()
        response_date['last_name'] = us.getlastname()
        use = StepUser.objects.get(stepUser__username=username)
        response_date['age'] = use.getage()
        response_date['city'] = use.getcity()
        response_date['allsteps'] = use.getsteps()
        response_date['photo'] = use.getphotourl()
        usid = use.getid()
        ol = StepUserHistory.objects.filter(user__id=usid).filter(date=dt)
        if ol.count() > 0:
            response_date['step'] = StepUserHistory.objects.filter(user__id=usid).get(date=dt).getsteps()
        else:
            response_date['step'] = 0
        # return HttpResponse(json.dumps(response_date), content_type="application/json", status_code=422)
    # response_date['error'] = "Успешно"
    return HttpResponse(json.dumps(response_date), content_type="application/json")


@csrf_exempt
def history(request):
    s = []
    if request.method == 'POST':
        username = request.POST.get('user', '')
        password =request.POST.get('password', '')
        usid = StepUser.objects.get(stepUser__username=username).getid()
        steps = StepUserHistory.objects.filter(user__id=usid)
        for step in steps:
            b = {}
            st = step.getsteps()
            dt = step.getdate()
            dat = int(time.mktime(dt.timetuple())*1000)

            b['date'] = dat
            b['step'] = st
            s.append(b)
    return HttpResponse(json.dumps(s), content_type="application/json", status=200)
