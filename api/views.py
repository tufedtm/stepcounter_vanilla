# coding:utf8
from __future__ import unicode_literals
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, render
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

            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)

            response['first_name'] = first_name
            response['last_name'] = last_name
            response['age'] = 0
            response['city'] = ''
            response['photo'] = ''
            response['steps_all'] = 0
            response['steps_today'] = 0

    return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def api_info(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            step_user = authenticate(username=username, password=password).stepuser

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
        except AttributeError:
            response['error'] = 'Неверный логин или пароль'
            return HttpResponse(json.dumps(response))

    return HttpResponse(json.dumps(response))


@csrf_exempt
def api_info_update(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            step_user = authenticate(username=username, password=password).stepuser

            step_user.user.first_name = request.POST.get('first_name')
            step_user.user.last_name = request.POST.get('last_name')
            step_user.age = request.POST.get('age')
            step_user.city = request.POST.get('city')
            step_user.save()
            step_user.user.save()

            response['first_name'] = request.POST.get('first_name')
            response['last_name'] = request.POST.get('last_name')
            response['age'] = request.POST.get('age')
            response['city'] = request.POST.get('city')

        except AttributeError:
            response['error'] = 'Неверный логин или пароль'
            return HttpResponse(json.dumps(response))

    return HttpResponse(json.dumps(response))


@csrf_exempt
def api_steps_update(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        steps = int(request.POST.get('steps'))

        try:
            step_user = authenticate(username=username, password=password).stepuser

            step_history = StepUserHistory(step_user_id=step_user.id, steps=steps, date=timezone.now().today())
            step_history.save()

            step_user.steps += steps
            step_user.save()

            response['steps'] = steps
            response['date'] = step_history.date.isoformat()

        except AttributeError:
            response['error'] = 'Неверный логин или пароль'
            return HttpResponse(json.dumps(response))

    return HttpResponse(json.dumps(response))


@csrf_exempt
def api_history(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            step_user = authenticate(username=username, password=password).stepuser
            step_user_history = StepUserHistory.objects.filter(step_user__user__username=step_user)

            for i, item in enumerate(step_user_history):
                response[i] = {
                    'date': item.date.isoformat(),
                    'steps': int(item.steps),
                }
        except:
            response['error'] = 'Неверный логин или пароль'
            return HttpResponse(json.dumps(response))

    return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def testy(request):
    return render(request, 'api/test.html')
